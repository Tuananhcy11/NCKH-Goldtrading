# CƠ SỞ LÝ LUẬN CỦA MÔ HÌNH VÀ THIẾT KẾ THỰC NGHIỆM

**Đề tài:** So sánh và đánh giá hiệu quả giữa chiến lược giao dịch dựa trên tín hiệu kỹ thuật (signal-based) và chiến lược dựa trên trí tuệ nhân tạo (AI-based) trong giao dịch vàng

**Dữ liệu:** `gold_price_2015_2025_cleaned (1).csv` — 4016 quan sát, 02/01/2015 → 30/12/2025
**Chương trình:** `ai_vs_ta_original_data.py`

---

## 1. Cơ sở lý luận về khả năng dự báo của thị trường

### 1.1. Giả thuyết Thị trường Hiệu quả (Efficient Market Hypothesis — Fama, 1970)

EMH dạng yếu (weak-form) phát biểu rằng giá hiện tại đã phản ánh toàn bộ thông tin chứa trong dữ liệu giá quá khứ. Nếu EMH dạng yếu đúng tuyệt đối, mọi chỉ báo kỹ thuật — vốn là hàm số của chuỗi giá quá khứ — đều **không** có năng lực dự báo, và chuỗi lợi suất phải là một martingale với tự tương quan bằng không.

Hệ quả phương pháp luận: **tự tương quan của log-return là thước đo trực tiếp mức độ không hiệu quả của thị trường.** Đây là lý do nhóm đặc trưng trễ (mục 3.4) vừa là biến dự báo, vừa là công cụ kiểm định giả thuyết.

### 1.2. Giả thuyết Thị trường Thích nghi (Adaptive Market Hypothesis — Lo, 2004)

AMH lập luận rằng hiệu quả thị trường không phải trạng thái tĩnh mà biến đổi theo thời gian: các cơ hội sinh lợi xuất hiện, bị khai thác, rồi biến mất khi đủ nhiều người tham gia. Quan hệ giữa tín hiệu và lợi nhuận vì thế **không dừng (non-stationary)**.

Hệ quả phương pháp luận: mô hình phải được **tái huấn luyện định kỳ** thay vì huấn luyện một lần. Đây là cơ sở của thiết kế walk-forward với chu kỳ tái huấn luyện (mục 5).

### 1.3. Cơ sở của phân tích kỹ thuật

Phân tích kỹ thuật dựa trên ba tiền đề (Lý thuyết Dow, Murphy 1999):
1. Giá phản ánh mọi thông tin và tâm lý thị trường.
2. Giá vận động theo xu hướng có **quán tính** (momentum) — cơ sở của nhóm chỉ báo xu hướng.
3. Lịch sử có tính lặp lại do tâm lý nhà đầu tư lặp lại — cơ sở của nhóm dao động.

Hai trường phái đối lập cùng tồn tại trong thực tiễn:
- **Trend-following:** giá đang tăng sẽ tiếp tục tăng (khai thác quán tính).
- **Mean-reversion:** giá bị đẩy quá xa giá trị trung bình sẽ quay trở lại (khai thác phản ứng thái quá).

Nghiên cứu này chọn benchmark từ **cả hai trường phái** (mục 6.2) để phép so sánh với AI không bị thiên lệch về một giả thuyết hành vi giá duy nhất.

---

## 2. Cơ sở lý luận về biến mục tiêu

### 2.1. Vì sao dùng log-return

$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$

Ba lý do:
1. **Tính cộng dồn theo thời gian:** lợi suất nhiều kỳ bằng tổng lợi suất từng kỳ, $r_{t \to t+k} = \sum r_i$. Điều này cho phép cộng dồn trực tiếp khi tính đường equity, trong khi lợi suất số học phải nhân dồn.
2. **Ổn định phương sai:** log-return giảm ảnh hưởng của mức giá tuyệt đối. Giá vàng đi từ ~1200 (2015) lên ~4000 (2025); nếu dùng chênh lệch tuyệt đối, phương sai sẽ tăng theo mức giá, vi phạm giả định đồng nhất phương sai.
3. **Tính đối xứng:** một mức tăng và giảm cùng độ lớn theo log là đối xứng, phù hợp với bài toán phân loại hai lớp cân bằng về mặt hình học.

### 2.2. Vì sao phân loại nhị phân thay vì hồi quy

$$\text{target}_t = \begin{cases} 1 & \text{nếu } r_{t+1} > 0 \\ 0 & \text{nếu } r_{t+1} \le 0 \end{cases}$$

Lập luận theo **hàm mục tiêu của người ra quyết định**: quyết định giao dịch Long/Flat chỉ phụ thuộc vào **dấu** của lợi nhuận kỳ vọng, không phụ thuộc độ lớn. Mô hình hồi quy tối thiểu hóa MSE sẽ dành phần lớn "năng lực" để dự báo đúng các cú biến động lớn (vì bình phương sai số phạt nặng outlier), trong khi mục tiêu giao dịch là dự báo đúng hướng ở **đa số phiên**. Hai hàm mục tiêu này không đồng nhất; do đó tối ưu hóa hồi quy không tối ưu hóa hiệu quả giao dịch.

### 2.3. Ràng buộc chống rò rỉ thông tin

Nhãn tại thời điểm $t$ mô tả **tương lai** $t+1$. Vì vậy mọi đặc trưng tại $t$ bắt buộc chỉ được tính từ thông tin đến hết $t$. Điều này được thực thi bằng hai cơ chế: (a) mọi cửa sổ trượt đều là cửa sổ đóng lùi về quá khứ; (b) thiết kế walk-forward ở mục 5.

---

## 3. Cơ sở lý luận về tập đặc trưng

Bốn nhóm đặc trưng được thiết kế để bao phủ bốn chiều thông tin độc lập của chuỗi giá.

### 3.1. Nhóm 1 — Chỉ báo xu hướng (Trend)

**Biến:** `MA10_MA30_diff`, `MA30_MA50_diff`, `EMA12_EMA26_diff`, `price_MA10_dist`

**Lý luận:** Trung bình động là bộ lọc thông thấp (low-pass filter), làm trơn nhiễu ngắn hạn để bóc tách thành phần xu hướng. EMA gán trọng số suy giảm theo hàm mũ cho các quan sát xa hơn, do đó phản ứng nhanh hơn MA khi thị trường đổi chế độ:

$$\text{EMA}_t = \alpha P_t + (1-\alpha)\text{EMA}_{t-1}, \quad \alpha = \frac{2}{n+1}$$

**Quyết định thiết kế quan trọng — dùng chênh lệch tương đối (%), không dùng giá trị tuyệt đối.** Hai lý do:

1. **Chống trôi khái niệm (concept drift).** Cây quyết định chia không gian bằng ngưỡng tuyệt đối dạng "MA10 < c". Mức giá vàng 2015 (~1200) và 2025 (~4000) khác nhau hơn ba lần, nên ngưỡng $c$ học được từ quá khứ trở nên vô nghĩa ở tương lai. Chuẩn hóa về tỷ lệ phần trăm khiến biến trở nên **bất biến theo mức giá (scale-invariant)**.

2. **Cung cấp sẵn quan hệ tương tác.** Chênh lệch MA ngắn − MA dài chính là định nghĩa toán học của tín hiệu giao cắt. Nếu chỉ đưa vào MA10 và MA30 riêng lẻ, mô hình cây phải xấp xỉ mặt phân chia chéo $MA_{10} - MA_{30} = 0$ bằng nhiều lần chia trực giao — kém hiệu quả về mặt thống kê. Đưa trực tiếp hiệu số giúp mô hình chỉ cần **một** lần chia tại ngưỡng 0.

### 3.2. Nhóm 2 — Chỉ báo động lượng và dao động (Momentum & Oscillator)

**Biến:** `RSI14`, `MACD_norm`, `MACD_hist_norm`

**RSI (Wilder, 1978):**

$$\text{RSI} = 100 - \frac{100}{1 + RS}, \quad RS = \frac{\overline{\text{Gain}}_{14}}{\overline{\text{Loss}}_{14}}$$

RSI chuẩn hóa nội tại về khoảng $[0, 100]$, đo tương quan giữa lực mua và lực bán. Vùng RSI < 30 (quá bán) và > 70 (quá mua) là cơ sở định lượng của giả thuyết hồi quy về trung bình. Ưu điểm với mô hình cây: thang đo cố định theo thời gian nên ngưỡng chia học được vẫn có hiệu lực ở tương lai — khác với các biến dựa trên mức giá.

**MACD (Appel, 1979):** $\text{MACD} = \text{EMA}_{12} - \text{EMA}_{26}$ đo khoảng cách hai đường trung bình, biểu diễn **gia tốc** của xu hướng. Histogram $\text{MACD} - \text{Signal}_9$ tương ứng đạo hàm bậc hai, có khả năng phát hiện phân kỳ (divergence) trước khi giá đảo chiều.

**Chuẩn hóa MACD theo giá** (`MACD/Close`): MACD nguyên bản có đơn vị là đơn vị giá, nên biên độ của nó tỷ lệ với mức giá. Không chuẩn hóa sẽ tái lập chính vấn đề concept drift đã nêu ở 3.1.

### 3.3. Nhóm 3 — Chỉ báo độ biến động (Volatility)

**Biến:** `BB_width`, `BB_pctB`, `volatility_20d`, `volume_ratio`

**Lý luận chế độ thị trường (market regime).** Đây là nhóm có cơ sở lý luận tinh tế nhất và thường bị bỏ sót. Luận điểm: quan hệ giữa chỉ báo và hướng giá **không ổn định mà phụ thuộc trạng thái biến động**. Cùng một tín hiệu MACD dương mang ý nghĩa khác nhau trong chế độ biến động thấp (xu hướng bền) so với chế độ biến động cao (nhiễu lớn, dễ đảo chiều).

Vì cây quyết định phân chia không gian đặc trưng thành các vùng rời rạc rồi học quy tắc riêng cho từng vùng, việc cung cấp biến biến động cho phép mô hình học **quy tắc có điều kiện theo chế độ**:

> *Nếu* biến động < ngưỡng, *thì* tín hiệu xu hướng đáng tin cậy; *ngược lại* thì không.

Đây chính là loại tương tác phi tuyến mà mô hình tuyến tính (logistic regression) **không thể** biểu diễn nếu không tạo biến tương tác thủ công. Nói cách khác, nhóm biến động là điều kiện để phát huy lợi thế cấu trúc của mô hình cây.

**Cơ sở thống kê cho tính dự báo:** hiện tượng **tụ cụm biến động (volatility clustering)** — biến động cao có xu hướng theo sau biến động cao (Mandelbrot 1963; Engle 1982, mô hình ARCH). Do đó `volatility_20d` là biến có tính bền vững, dự báo được, khác với chuỗi lợi suất gần như ngẫu nhiên.

**Bollinger Bands (Bollinger, 1980s):** `BB_pctB` định vị giá trong dải $[\mu_{20} \pm 2\sigma_{20}]$, tức là **z-score chuẩn hóa** của giá — thước đo mức độ lệch khỏi trung bình theo đơn vị độ lệch chuẩn. `BB_width` đo độ rộng dải, là chỉ báo trực tiếp của chế độ biến động (hiện tượng "squeeze" báo hiệu biến động sắp tăng).

**`volume_ratio`** (khối lượng / trung bình 20 kỳ): khối lượng xác nhận độ tin cậy của chuyển động giá. Chuẩn hóa theo trung bình trượt vì khối lượng tuyệt đối có xu hướng tăng dài hạn.

### 3.4. Nhóm 4 — Đặc trưng trễ (Lagged features)

**Biến:** `log_return_lag1`, `log_return_lag2`, `log_return_lag3`

**Lý luận:** Nhóm này nắm bắt cấu trúc tự tương quan bậc thấp của chuỗi lợi suất — thành phần thông tin mà bốn nhóm trên (đều là biến đã làm trơn) không biểu diễn được.

Theo EMH dạng yếu (1.1), hệ số tự tương quan phải bằng 0. Do đó **độ lớn đóng góp của nhóm này là thước đo định lượng mức độ không hiệu quả của thị trường** — nó vừa là biến dự báo, vừa là kết quả kiểm định giả thuyết.

**Cảnh báo phương pháp luận:** nếu nhóm trễ có Gain áp đảo bất thường, phải kiểm tra xem đó là tín hiệu thị trường thật hay hiện tượng nhân tạo do quy trình xử lý dữ liệu (xem mục 4 và mục 10).

---

## 4. Cơ sở lý luận về kiểm định chất lượng dữ liệu

**Nguyên tắc:** trước khi diễn giải bất kỳ kết quả dự báo nào, phải kiểm định xem cấu trúc dự báo có nguồn gốc từ **thị trường** hay từ **quy trình xử lý dữ liệu**. Bỏ qua bước này là nguyên nhân phổ biến nhất của kết quả nghiên cứu không thể tái lập trong tài chính định lượng.

Ba phép kiểm định chuẩn được thực hiện (Chương 4 của chương trình):

| Phép kiểm định | Ngưỡng kỳ vọng (dữ liệu thật) | Kết quả trên dataset gốc |
|---|---|---|
| (a) Tỷ lệ bước giá trùng bước trước | ~0% | **76.07%** |
| (b) Tự tương quan log-return lag1 | $\lvert\rho\rvert < 0.05$ | 0.0415 |
| (c) Số quan sát vào T7 + CN | 0 | **1148** |
| (d) Tỷ lệ ngày tăng | ~52–53% | **66.13%** |

**Diễn giải (a) và (c):** hợp đồng vàng COMEX không giao dịch cuối tuần, nên dữ liệu thật không thể có quan sát T7/CN. Việc 76.07% bước giá trùng đúng bước trước là dấu hiệu của **nội suy tuyến tính**: giá các ngày không giao dịch được điền bằng cách chia đều khoảng cách giữa hai ngày giao dịch liền kề.

Minh chứng cụ thể từ bốn quan sát đầu:

| Ngày | Thứ | Close | Bước nhảy |
|---|---|---|---|
| 02/01/2015 | Sáu | 1186.000 | — |
| 03/01/2015 | **Bảy** | 1191.967 | +5.966675 |
| 04/01/2015 | **CN** | 1197.933 | +5.966675 |
| 05/01/2015 | Hai | 1203.900 | +5.966675 |

**Hệ quả lý thuyết — rò rỉ thông tin tương lai (look-ahead leakage):** giá ngày T7 và CN được suy ra từ giá ngày **thứ Hai kế sau**, tức là từ thông tin chưa tồn tại tại thời điểm đó. Trong các đoạn nội suy, quan hệ $r_{t+1} = r_t$ đúng một cách xác định. Mô hình do đó có thể đạt độ chính xác rất cao chỉ bằng cách nhận diện "đang ở trong đoạn nội suy" — một năng lực **không tồn tại** trên thị trường thực.

Đây là lý do tỷ lệ ngày tăng đạt 66.13% thay vì ~53%: mỗi lần giá tăng qua cuối tuần, phép nội suy tạo ra ba ngày tăng liên tiếp thay vì một.

---

## 5. Cơ sở lý luận về thiết kế kiểm định (Walk-forward)

### 5.1. Vì sao không dùng K-Fold Cross-Validation ngẫu nhiên

K-Fold ngẫu nhiên giả định các quan sát **độc lập và cùng phân phối (i.i.d.)** — giả định bị vi phạm hoàn toàn với chuỗi thời gian. Khi trộn ngẫu nhiên, tập huấn luyện chứa các quan sát xảy ra **sau** tập kiểm định, tạo look-ahead bias và làm kết quả bị phóng đại một cách hệ thống. Ngoài ra, tự tương quan giữa các quan sát gần nhau khiến tập train và test không độc lập, làm ước lượng sai số quá lạc quan.

### 5.2. Thiết kế walk-forward với cửa sổ mở rộng

$$\text{Huấn luyện trên } [0, t) \;\longrightarrow\; \text{Dự báo } [t, t+h) \;\longrightarrow\; t \leftarrow t + h$$

**Tham số:** tập huấn luyện ban đầu 1825 quan sát (~5 năm), tái huấn luyện mỗi 365 quan sát (~1 năm).

**Ba lý do:**
1. **Mô phỏng đúng điều kiện thực tế:** tại mọi thời điểm ra quyết định, nhà giao dịch chỉ có dữ liệu quá khứ. Walk-forward là thiết kế duy nhất tôn trọng ràng buộc nhân quả theo thời gian.
2. **Thích nghi với concept drift:** tái huấn luyện định kỳ cho phép mô hình cập nhật theo chế độ thị trường mới — trực tiếp hiện thực hóa hàm ý của AMH (mục 1.2).
3. **Chuỗi out-of-sample dài liên tục:** cho phép backtest chiến lược trên một chuỗi thời gian thực sự chưa từng được mô hình thấy, thay vì chỉ một tập test đơn lẻ.

### 5.3. Cơ sở lựa chọn siêu tham số XGBoost

| Tham số | Giá trị | Cơ sở lý luận |
|---|---|---|
| `max_depth` | 3 | Dữ liệu tài chính có tỷ lệ tín hiệu/nhiễu rất thấp. Cây sâu sẽ khớp nhiễu. Cây nông buộc mô hình học quy tắc tổng quát. |
| `learning_rate` | 0.05 | Mỗi cây đóng góp nhỏ → hội tụ ổn định, giảm phương sai của mô hình tổng. |
| `n_estimators` | 200 | Kết hợp với learning rate thấp để đủ năng lực học mà không quá khớp. |
| `subsample`, `colsample_bytree` | 0.8 | Lấy mẫu ngẫu nhiên theo hàng và cột → giảm tương quan giữa các cây, tăng tính tổng quát. |
| `reg_lambda` | 1.0 | Ràng buộc L2 lên trọng số lá, hạn chế lá có giá trị cực trị do ít mẫu. |
| `min_child_weight` | 5 | Yêu cầu tối thiểu số mẫu (theo trọng số Hessian) tại lá → tránh lá học từ vài quan sát nhiễu. |
| `scale_pos_weight` | $n_-/n_+$ | Xử lý mất cân bằng lớp, tránh mô hình suy biến thành "luôn dự báo lớp đa số". |

---

## 6. Cơ sở lý luận về xây dựng chiến lược giao dịch

### 6.1. Quy ước thực thi — điều kiện tiên quyết cho tính trung thực của backtest

Tín hiệu tại ngày $t$ được tính từ thông tin đến hết ngày $t$ (giá đóng cửa $t$). Vị thế được mở tại giá đóng cửa $t$ và nắm giữ suốt ngày $t+1$:

$$r^{\text{strat}}_t = \text{position}_{t-1} \times r_t$$

Nếu viết sai thành $\text{position}_t \times r_t$, tín hiệu sẽ "biết trước" lợi nhuận cùng kỳ và toàn bộ kết quả backtest trở nên vô nghĩa. Đây là lỗi phổ biến nhất trong backtest.

### 6.2. Cơ sở lựa chọn các chiến lược benchmark

| Chiến lược | Trường phái | Giả thuyết hành vi giá |
|---|---|---|
| **MA Crossover** (MA10 vs MA30) | Trend-following | Xu hướng có quán tính |
| **MACD Crossover** | Trend-following | Như trên, phản ứng nhanh hơn nhờ EMA |
| **RSI (30/70)** | Mean-reversion | Giá bị đẩy quá xa sẽ quay lại |
| **Combined** (MA ∧ MACD) | Trend-following có xác nhận kép | Giảm tín hiệu giả, đổi lại giảm số cơ hội |
| **Buy & Hold** | Thụ động | Benchmark bắt buộc |

Việc chọn benchmark từ **cả hai trường phái đối lập** là yêu cầu về tính công bằng: nếu chỉ so với trend-following, kết luận sẽ phụ thuộc vào việc giai đoạn kiểm định có xu hướng rõ hay không.

**Vai trò của Buy & Hold:** đây là benchmark **không thể bỏ qua**. Một chiến lược chủ động chỉ tạo ra giá trị kinh tế nếu vượt được Buy & Hold **sau chi phí giao dịch**. Nếu không, nhà đầu tư hợp lý sẽ chọn nắm giữ thụ động với chi phí gần bằng không.

### 6.3. Cơ sở của biến thể lọc độ tin cậy (`AI_XGB_Conf60`)

Khi xác suất dự báo gần 0.5, lợi nhuận kỳ vọng của giao dịch không đủ bù chi phí. Chỉ giao dịch khi $P(\text{up}) > 0.60$ làm giảm turnover, do đó giảm ma sát chi phí. Đây là ứng dụng của nguyên tắc: **chỉ hành động khi lợi thế kỳ vọng vượt ngưỡng chi phí giao dịch.**

### 6.4. Cơ sở của việc tính chi phí giao dịch

$$\text{cost}_t = \lvert \text{position}_t - \text{position}_{t-1} \rvert \times \text{cost bps}$$

Bỏ qua chi phí là lỗi làm sai lệch backtest nghiêm trọng nhất, đặc biệt với chiến lược AI có turnover cao (mục 9 cho thấy AI có turnover ~37 lần/năm so với ~5 của MA Crossover). Mức 2 bps (0.02%) mỗi lần đổi vị thế phản ánh spread điển hình của hợp đồng vàng tương lai thanh khoản cao.

---

## 7. Cơ sở lý luận về các chỉ tiêu đánh giá

Nghiên cứu dùng đồng thời nhiều chỉ tiêu vì **không một chỉ tiêu đơn lẻ nào đủ** để mô tả hiệu quả chiến lược: một chiến lược có thể có Sharpe cao nhưng mức sụt giảm không thể chấp nhận về mặt tâm lý.

### 7.1. Nhóm chỉ tiêu lợi nhuận

- **Total Return:** lợi nhuận tích lũy toàn kỳ.
- **CAGR** $= (\text{Equity}_T)^{P/n} - 1$: chuẩn hóa lợi nhuận theo thời gian, cho phép so sánh các giai đoạn khác độ dài.

### 7.2. Nhóm chỉ tiêu rủi ro

- **Ann. Volatility** $= \sigma(r) \sqrt{P}$: độ lệch chuẩn lợi suất — rủi ro tổng thể.
- **Max Drawdown** $= \min_t \left( \frac{E_t}{\max_{s \le t} E_s} - 1 \right)$: mức sụt giảm tối đa từ đỉnh. Đây là thước đo rủi ro **dưới dạng trải nghiệm** — nó quyết định khả năng nhà giao dịch trụ lại với chiến lược trong thực tế, điều mà độ lệch chuẩn không phản ánh.

### 7.3. Nhóm chỉ tiêu hiệu quả điều chỉnh rủi ro

**Sharpe Ratio** (Sharpe, 1966):

$$SR = \frac{E[r] - r_f}{\sigma(r)} \sqrt{P}$$

Lợi nhuận trên một đơn vị rủi ro tổng. Là thước đo phổ biến nhất, nhưng có hai hạn chế cần nêu: (a) phạt cả biến động **tăng** (upside volatility), điều nhà đầu tư không coi là rủi ro; (b) giả định lợi suất xấp xỉ phân phối chuẩn, trong khi lợi suất tài chính có đuôi dày.

**Sortino Ratio:** thay $\sigma(r)$ bằng độ lệch chuẩn phần âm (downside deviation), khắc phục hạn chế (a). Phù hợp hơn với cảm nhận rủi ro thực tế: nhà đầu tư chỉ sợ lỗ, không sợ lãi.

**Calmar Ratio** $= \text{CAGR} / \lvert \text{MaxDD} \rvert$: lợi nhuận trên một đơn vị rủi ro sụt giảm. Bổ trợ Sharpe ở chiều rủi ro trải nghiệm.

### 7.4. Cơ sở của hệ số quy đổi năm $P = 365$

Đây là điểm kỹ thuật **bắt buộc phải xử lý đúng**. Sharpe và Volatility hàng năm được quy đổi bằng $\sqrt{P}$, trong đó $P$ là **số quan sát thực tế trong một năm của chuỗi dữ liệu**.

Dataset gốc chứa cả T7/CN nên có ~365 quan sát/năm, không phải 252 như dữ liệu phiên giao dịch thực. Dùng sai $P = 252$ sẽ làm Sharpe bị lệch theo tỷ lệ $\sqrt{365/252} \approx 1.20$, tức **phóng đại khoảng 20%**. Chương trình đặt `PERIODS_PER_YEAR = 365` để khớp với tần số quan sát thật của chuỗi.

### 7.5. Cơ sở của chỉ tiêu tính ổn định

Tiêu chí thứ ba trong mục tiêu đề tài. Một chiến lược có thể đạt Sharpe cao toàn kỳ nhờ một vài giai đoạn bất thường. Tính ổn định được đo bằng ba chỉ tiêu bổ trợ:
1. **Lợi nhuận từng năm** — kiểm tra hiệu năng có đều không.
2. **Độ lệch chuẩn lợi nhuận năm** — càng nhỏ càng ổn định.
3. **Tỷ lệ năm có lãi** và **năm xấu nhất** — đo rủi ro đuôi theo năm.

---

## 8. Cơ sở lý luận về diễn giải mô hình

### 8.1. Ablation Study — thiết kế nhân quả để đo đóng góp biến

**Vì sao Feature Importance nội bộ không đủ.** Gain Importance chỉ cho biết mô hình **đã dùng** biến nào nhiều, không cho biết biến đó có **cải thiện năng lực dự báo ngoài mẫu** hay không. Một biến hoàn toàn là nhiễu vẫn có thể có Gain dương do mô hình quá khớp vào nó.

**Ablation study** — huấn luyện lại từ đầu với từng tập con đặc trưng rồi so sánh hiệu năng out-of-sample — là thiết kế đúng để định lượng đóng góp. Nghiên cứu cộng dồn theo nhóm để đọc được **giá trị gia tăng** của từng nhóm:

$$M_1 \subset M_2 \subset M_3 \subset M_4$$

Điểm then chốt: mỗi mô hình được huấn luyện lại **với cùng thiết kế walk-forward**, nên chênh lệch AUC giữa các bậc là ước lượng không chệch của giá trị gia tăng.

### 8.2. SHAP — phân rã dự báo theo lý thuyết trò chơi hợp tác

SHAP (Lundberg & Lee, 2017) phân rã mỗi dự báo thành tổng đóng góp của từng biến dựa trên **giá trị Shapley** trong lý thuyết trò chơi hợp tác:

$$f(x) = \phi_0 + \sum_{j=1}^{M} \phi_j$$

Ba ưu điểm so với Gain Importance:
1. **Tính cộng (additivity):** tổng đóng góp bằng đúng chênh lệch giữa dự báo và giá trị cơ sở.
2. **Tính nhất quán (consistency):** nếu một biến đóng góp nhiều hơn trong mọi tập con, giá trị SHAP của nó phải lớn hơn — tính chất mà Gain không bảo đảm.
3. **Cho biết chiều tác động** trên **từng quan sát**, không chỉ độ lớn tổng hợp. Điều này cho phép kiểm tra xem mô hình có học đúng quan hệ kinh tế (ví dụ: RSI thấp → xác suất tăng giá cao, phù hợp giả thuyết hồi quy về trung bình) hay chỉ khớp nhiễu.

---

## 9. Kết quả thực nghiệm

**Giai đoạn out-of-sample:** 19/02/2020 → 29/12/2025 (2141 quan sát)
**Hệ số quy đổi năm:** 365 · **Chi phí giao dịch:** 2 bps/lần

### 9.1. Chất lượng dự báo của mô hình

| Chỉ tiêu | Giá trị |
|---|---|
| Accuracy | 0.8389 |
| F1-score | 0.8862 |
| AUC | 0.9299 |
| Baseline (luôn dự báo lớp đa số) | ~0.66 |

### 9.2. Ablation Study

| Mô hình | Số đặc trưng | Accuracy | F1 | AUC | AUC gia tăng |
|---|---|---|---|---|---|
| M1 — Xu hướng | 4 | 0.6240 | 0.6943 | 0.7989 | — |
| M2 — + Động lượng | 7 | 0.8108 | 0.8649 | 0.9117 | **+0.1128** |
| M3 — + Biến động | 11 | 0.8062 | 0.8597 | 0.9112 | −0.0005 |
| M4 — + Trễ (đầy đủ) | 14 | **0.8389** | **0.8862** | **0.9299** | +0.0187 |

**Diễn giải:** nhóm **động lượng** đóng góp lớn nhất (+0.1128 AUC) — chủ yếu từ RSI. Nhóm **biến động** không cải thiện AUC trực tiếp (−0.0005) nhưng đóng góp 14.85% Gain, cho thấy vai trò của nó là **điều kiện hóa** các tín hiệu khác theo chế độ thị trường chứ không phải dự báo độc lập. Nhóm **trễ** thêm +0.0187.

### 9.3. Gain Importance theo nhóm

| Nhóm | % Gain |
|---|---|
| 2 — Động lượng | 54.66% |
| 4 — Trễ | 22.63% |
| 3 — Biến động | 14.85% |
| 1 — Xu hướng | 7.86% |

Biến đơn lẻ quan trọng nhất: `RSI14` (51.05%), `log_return_lag1` (19.06%), `volatility_20d` (7.16%).

### 9.4. Bảng so sánh hiệu quả chiến lược

| Chiến lược | Total Return | CAGR | Ann. Vol | **Sharpe** | Sortino | **Max DD** | Calmar | Win Rate | Số lệnh | Turnover/năm |
|---|---|---|---|---|---|---|---|---|---|---|
| **AI_XGB_Conf60** | 127.91% | 15.08% | 3.09% | **4.568** | 1.929 | **−4.79%** | **3.151** | 91.53% | 130 | 22.2 |
| **AI_XGB_LongFlat** | 144.35% | 16.45% | 4.69% | 3.270 | 1.726 | −7.44% | 2.212 | 86.13% | 218 | 37.2 |
| TA_MA_Crossover | 189.15% | 19.84% | 6.99% | 2.624 | 1.434 | −7.21% | 2.754 | 86.82% | 29 | 4.9 |
| BuyHold | 174.64% | 18.80% | 8.34% | 2.107 | 1.784 | −17.82% | 1.055 | 74.08% | 1 | 0.2 |
| AI_XGB_LongShort | 117.40% | 14.16% | 8.38% | 1.621 | 1.321 | −14.12% | 1.003 | 83.25% | 218 | 74.2 |
| TA_Combined | 65.54% | 8.97% | 5.80% | 1.511 | 0.654 | −9.16% | 0.980 | 80.60% | 58 | 9.9 |
| TA_MACD | 69.63% | 9.43% | 6.50% | 1.418 | 0.715 | −15.49% | 0.608 | 77.66% | 64 | 10.9 |
| TA_RSI | −2.02% | −0.35% | 4.87% | −0.047 | −0.035 | −20.27% | −0.017 | 27.88% | 22 | 3.8 |

### 9.5. Tính ổn định — lợi nhuận theo năm (%)

| Năm | BuyHold | TA_MA_Cross | TA_MACD | TA_RSI | TA_Combined | AI_LongFlat | AI_LongShort | AI_Conf60 |
|---|---|---|---|---|---|---|---|---|
| 2020 | 17.74 | 20.70 | −1.92 | 0.48 | −2.08 | 15.41 | 13.12 | 15.48 |
| 2021 | −3.47 | 2.88 | −1.93 | −4.77 | 4.77 | 1.86 | 7.47 | 9.43 |
| 2022 | −0.15 | 8.35 | −1.44 | −7.06 | −5.50 | 6.80 | 14.24 | 1.95 |
| 2023 | 13.08 | 6.74 | 11.67 | 3.01 | 9.11 | 7.32 | 1.85 | 7.52 |
| 2024 | 27.42 | 22.31 | 5.92 | 5.78 | 4.25 | 23.17 | 19.06 | 20.75 |
| 2025 | 67.95 | 64.62 | 51.27 | 1.11 | 50.11 | 47.23 | 29.07 | 36.25 |

| Chiến lược | Độ lệch chuẩn LN năm | Tỷ lệ năm có lãi | Năm xấu nhất |
|---|---|---|---|
| TA_RSI | 4.82 | 66.67% | −7.06% |
| AI_XGB_LongShort | 9.42 | **100%** | +1.85% |
| AI_XGB_Conf60 | 12.18 | **100%** | +1.95% |
| AI_XGB_LongFlat | 16.62 | **100%** | +1.86% |
| TA_Combined | 20.28 | 66.67% | −5.50% |
| TA_MACD | 20.67 | 50.00% | −1.93% |
| TA_MA_Crossover | 22.79 | 100% | +2.88% |
| BuyHold | 25.93 | 66.67% | −3.47% |

### 9.6. Nhận định theo ba tiêu chí của đề tài

**Lợi nhuận:** TA_MA_Crossover cho tổng lợi nhuận cao nhất (189.15%), vượt cả Buy & Hold (174.64%). Các chiến lược AI đạt 117–144%, thấp hơn về lợi nhuận thuần.

**Rủi ro:** các chiến lược AI vượt trội rõ rệt. `AI_XGB_Conf60` có độ biến động thấp nhất (3.09% so với 8.34% của Buy & Hold) và Max Drawdown nhỏ nhất (−4.79% so với −17.82%). Xét theo hiệu quả điều chỉnh rủi ro, AI dẫn đầu với Sharpe 4.568 và Calmar 3.151.

**Tính ổn định:** cả ba biến thể AI đều có **100% số năm có lãi** và năm xấu nhất vẫn dương — đặc tính mà không chiến lược kỹ thuật nào ngoài MA_Crossover đạt được. Ngược lại TA_MACD chỉ lãi 50% số năm.

**Kết luận sơ bộ:** chiến lược AI không thắng về lợi nhuận tuyệt đối nhưng **vượt trội về hiệu quả điều chỉnh rủi ro và tính ổn định**. Việc bổ sung bộ lọc độ tin cậy (`Conf60`) cải thiện đồng thời cả ba tiêu chí so với biến thể AI cơ bản, xác nhận lập luận ở mục 6.3.

---

## 10. Hạn chế của nghiên cứu

### 10.1. Hạn chế về chất lượng dữ liệu — cần nêu rõ trong báo cáo

Như trình bày ở mục 4, dataset chứa 1148 quan sát vào T7/CN và 76.07% bước giá là kết quả nội suy tuyến tính. Vì giá ngày không giao dịch được suy ra từ giá ngày giao dịch **kế sau**, tồn tại rò rỉ thông tin tương lai trong dữ liệu đầu vào.

**Hệ quả định lượng:** các chỉ số Accuracy (0.8389) và AUC (0.9299) **cao hơn đáng kể** so với năng lực dự báo thực tế. Để kiểm chứng, nhóm đã thực hiện thí nghiệm đối chứng trên dữ liệu vàng thật (2764 phiên giao dịch, nguồn Yahoo Finance `GC=F`, script `strategy_comparison.py`) với **cùng tập đặc trưng và cùng thiết kế walk-forward**:

| | Dataset gốc (có nội suy) | Dữ liệu thật (đối chứng) |
|---|---|---|
| Số quan sát | 4016 (~365/năm) | 2764 (~251/năm) |
| Tỷ lệ ngày tăng | 66.13% | 53.06% |
| **AUC** | **0.9299** | **0.5012** |
| **Accuracy** | **0.8389** | **0.5003** |
| Sharpe chiến lược AI | 3.270 | 0.576 |

Chênh lệch AUC từ 0.93 xuống 0.50 cho thấy **gần như toàn bộ năng lực dự báo quan sát được trên dataset gốc đến từ hiện tượng nội suy, không phải từ tín hiệu thị trường.** Trên dữ liệu thật, AUC 0.5012 tương đương ngẫu nhiên — kết quả này nhất quán với EMH dạng yếu (mục 1.1).

**Khuyến nghị:** kết quả ở mục 9 nên được trình bày như phân tích trên bộ dữ liệu được cung cấp, kèm phần đối chứng này. Nếu mục tiêu là kết luận về năng lực dự báo thực tế của AI trên thị trường vàng, cần sử dụng dữ liệu chỉ gồm phiên giao dịch thật.

### 10.2. Hạn chế về giai đoạn kiểm định

Giai đoạn out-of-sample (2020–2025) là **thị trường tăng giá mạnh** của vàng (Buy & Hold +174.64%, riêng 2025 +67.95%). Trong giai đoạn như vậy, mọi chiến lược có lúc đứng ngoài thị trường đều chịu bất lợi cấu trúc, còn chiến lược nắm giữ dài được ưu thế. Kết luận so sánh vì thế phụ thuộc vào đặc tính giai đoạn. Nên bổ sung giai đoạn đi ngang hoặc giảm (ví dụ 2013–2018) để kiểm định tính bền vững.

### 10.3. Các hạn chế khác

- **Chi phí giao dịch:** giả định 2 bps cố định, chưa mô hình hóa trượt giá (slippage) tăng theo quy mô lệnh và theo biến động. Với chiến lược AI có turnover 37 lần/năm, kết quả nhạy cảm với giả định này.
- **Chỉ dùng đặc trưng nội sinh:** toàn bộ đặc trưng là hàm của chuỗi giá và khối lượng. Chưa đưa vào biến ngoại sinh có cơ sở kinh tế đối với vàng: chỉ số USD (DXY), lợi suất thực trái phiếu Mỹ, chỉ số bất ổn (VIX). Đây là hướng mở rộng có cơ sở lý luận mạnh nhất, vì chỉ báo kỹ thuật không bổ sung thông tin ngoài chuỗi giá.
- **Chưa kiểm định ý nghĩa thống kê** của chênh lệch Sharpe giữa các chiến lược (có thể dùng kiểm định Jobson–Korkie hoặc bootstrap).
- **Chưa mô hình hóa position sizing** theo biến động; các chiến lược đều dùng vị thế toàn phần hoặc bằng không.

---

## 11. Tài liệu tham khảo

1. Fama, E. F. (1970). *Efficient Capital Markets: A Review of Theory and Empirical Work.* Journal of Finance, 25(2), 383–417.
2. Lo, A. W. (2004). *The Adaptive Markets Hypothesis.* Journal of Portfolio Management, 30(5), 15–29.
3. Chen, T., & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.* KDD '16.
4. Lundberg, S. M., & Lee, S. I. (2017). *A Unified Approach to Interpreting Model Predictions.* NeurIPS.
5. Sharpe, W. F. (1966). *Mutual Fund Performance.* Journal of Business, 39(1), 119–138.
6. Sortino, F. A., & Price, L. N. (1994). *Performance Measurement in a Downside Risk Framework.* Journal of Investing, 3(3), 59–64.
7. Engle, R. F. (1982). *Autoregressive Conditional Heteroskedasticity with Estimates of the Variance of UK Inflation.* Econometrica, 50(4), 987–1008.
8. Wilder, J. W. (1978). *New Concepts in Technical Trading Systems.* Trend Research.
9. Murphy, J. J. (1999). *Technical Analysis of the Financial Markets.* New York Institute of Finance.
10. Bailey, D. H., & López de Prado, M. (2014). *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality.* Journal of Portfolio Management, 40(5).
