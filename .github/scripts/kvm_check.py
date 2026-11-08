#!/usr/bin/env python3
"""Functional KVM preflight: can this process actually open /dev/kvm and talk to KVM?

Exit codes (each also prints a distinct ::error:: annotation):
  0 usable | 10 missing | 11 not a character device | 12 access denied
  13 open failed (other) | 14 KVM ioctl failed | 15 unexpected KVM API version
A pass means the KVM interface is accessible, not that the emulator will boot.
Dependencies are injectable so the logic can be exercised without real hardware.
"""
import errno
import os
import stat
import sys

KVM_GET_API_VERSION = 0xAE00  # _IO(KVMIO=0xAE, 0x00)
EXPECTED_API_VERSION = 12     # stable since Linux 2.6.22; the interface documents it as constant


def _fail(code, title, message):
    print(f"::error title={title}::{message}")
    return code


def check_kvm(path="/dev/kvm", *, stat_fn=os.stat, open_fn=os.open, close_fn=os.close, ioctl_fn=None):
    try:
        st = stat_fn(path)
    except FileNotFoundError:
        return _fail(10, "KVM device missing", f"{path} does not exist on this runner (no KVM exposed by the VM).")
    except OSError as exc:
        return _fail(13, "KVM stat failed", f"stat({path}) failed: errno {exc.errno} ({errno.errorcode.get(exc.errno, '?')}): {exc.strerror}")
    if not stat.S_ISCHR(st.st_mode):
        return _fail(11, "KVM not a character device", f"{path} exists but is not a character device (mode {stat.filemode(st.st_mode)}).")
    flags = os.O_RDWR | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = open_fn(path, flags)
    except PermissionError as exc:
        return _fail(12, "KVM access denied", f"open({path}, O_RDWR) denied: errno {exc.errno} ({errno.errorcode.get(exc.errno, '?')}): {exc.strerror}. "
                     "Runner user lacks rw access; udev rule may not have applied.")
    except OSError as exc:
        return _fail(13, "KVM open failed", f"open({path}, O_RDWR) failed: errno {exc.errno} ({errno.errorcode.get(exc.errno, '?')}): {exc.strerror}")
    try:
        if ioctl_fn is None:
            import fcntl
            ioctl_fn = fcntl.ioctl
        try:
            version = ioctl_fn(fd, KVM_GET_API_VERSION, 0)
        except OSError as exc:
            return _fail(14, "KVM ioctl failed", f"KVM_GET_API_VERSION failed: errno {exc.errno} ({errno.errorcode.get(exc.errno, '?')}): {exc.strerror}")
        except ImportError as exc:
            return _fail(14, "KVM ioctl unavailable", f"cannot issue ioctl: {exc}")
        if version != EXPECTED_API_VERSION:
            return _fail(15, "KVM API version unexpected", f"KVM_GET_API_VERSION returned {version}, expected {EXPECTED_API_VERSION}.")
        print(f"KVM usable: opened {path} O_RDWR, KVM_GET_API_VERSION={version}")
        return 0
    finally:
        close_fn(fd)


if __name__ == "__main__":
    sys.exit(check_kvm(os.environ.get("KVM_DEVICE", "/dev/kvm")))
