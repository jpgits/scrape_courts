from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class Judgment:
    裁判例集: str
    裁判種別: Optional[str] = None
    法廷名: Optional[str] = None
    裁判年月日: Optional[str] = None
    事件名: Optional[str] = None
    事件番号: Optional[str] = None
    判示事項: Optional[str] = None
    裁判要旨: Optional[str] = None
    結果: Optional[str] = None
    原審裁判所名: Optional[str] = None
    原審裁判年月日: Optional[str] = None
    原審事件番号: Optional[str] = None
    判例集等巻号頁: Optional[str] = None
    参照法条: Optional[str] = None
    全文: List[Dict[str, str]] = field(default_factory=list)
