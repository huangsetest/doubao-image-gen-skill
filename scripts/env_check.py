"""
豆包图像生成 - 辅助脚本
检查 browser-use 环境并连接 Chrome，输出就绪状态。
"""
import subprocess
import sys


def run(cmd: str, timeout: int = 30) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Timed out after {timeout}s"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd.split()[0]}"


def check_browser_use() -> bool:
    """Check if browser-use CLI is available."""
    code, out, err = run("browser-use doctor")
    if code == 0:
        print("[OK] browser-use is ready")
        return True
    print(f"[FAIL] browser-use check failed:\n{err or out}")
    return False


def connect_chrome() -> bool:
    """Connect to existing Chrome via CDP."""
    code, out, err = run("browser-use connect", timeout=15)
    if code == 0 or "connected" in (out + err).lower():
        print("[OK] Chrome connected via CDP")
        return True
    print(f"[FAIL] Cannot connect to Chrome:\n{err or out}")
    print("Make sure Chrome is running with --remote-debugging-port=9222")
    return False


def main():
    print("=== 豆包图像生成 - 环境检查 ===\n")

    if not check_browser_use():
        sys.exit(1)

    if not connect_chrome():
        sys.exit(1)

    print("\n[READY] 环境就绪，可以开始豆包图像生成流程。")


if __name__ == "__main__":
    main()