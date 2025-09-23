import os, csv

CSV_FIELDS = ["job_title","company","salary","location","posted","job_url","company_url","source_page","summary"]

class RealtimeCsvWriter:
    def __init__(self, path):
        self.path = path
        self.f = None
        self.w = None
        self._open()

    def _open(self):
        # Tạo file nếu chưa có và ghi header
        need_header = (not os.path.exists(self.path)) or os.path.getsize(self.path) == 0
        # buffering=1 = line buffered (chỉ áp dụng cho text mode)
        self.f = open(self.path, "a", encoding="utf-8", newline="", buffering=1)
        self.w = csv.DictWriter(self.f, fieldnames=CSV_FIELDS)
        if need_header:
            self.w.writeheader()
            self.f.flush()
            os.fsync(self.f.fileno())

    def write_row(self, row: dict):
        # Bảo đảm đủ cột (thiếu thì để rỗng)
        safe = {k: (row.get(k, "") or "") for k in CSV_FIELDS}
        self.w.writerow(safe)
        # ép ghi ngay ra đĩa
        self.f.flush()
        os.fsync(self.f.fileno())

    def close(self):
        try:
            if self.f:
                self.f.close()
        except:
            pass

def load_existing_urls_quick(path):
    urls = set()
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                u = (row.get("job_url") or "").strip()
                if u:
                    urls.add(u)
    return urls