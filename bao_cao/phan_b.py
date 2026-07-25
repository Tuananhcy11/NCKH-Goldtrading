# -*- coding: utf-8 -*-
"""PHAN B: Chuong 1 (co so ly thuyet) va Chuong 2 (du lieu, phuong phap)."""
from docx.shared import Pt
from engine import para, heading, bullet, table, figure, formula

IMG = "../ket_qua/goc/"


def chuong_1(doc):
    heading(doc, "CHƯƠNG 1. CƠ SỞ LÝ THUYẾT", level=1, align="center",
            page_break=True)

    # ---------------------------------------------------------------- 1.1
    heading(doc, "1.1. Lý thuyết về khả năng dự báo của thị trường", level=2)

    heading(doc, "1.1.1. Giả thuyết Thị trường Hiệu quả", level=3)
    para(doc,
         "Giả thuyết Thị trường Hiệu quả do Fama (1970) đề xuất phân biệt ba "
         "dạng hiệu quả tùy theo tập thông tin được phản ánh trong giá. Dạng yếu "
         "khẳng định giá hiện tại đã phản ánh toàn bộ thông tin chứa trong dữ "
         "liệu giá quá khứ. Nếu dạng yếu đúng tuyệt đối, chuỗi lợi suất là một "
         "martingale, nghĩa là kỳ vọng lợi suất tương lai khi biết toàn bộ quá "
         "khứ bằng không:")
    formula(doc, "E[r(t+1) | r(t), r(t−1), …] = 0")
    para(doc,
         "và hệ số tự tương quan của chuỗi lợi suất phải bằng không với mọi độ "
         "trễ:")
    formula(doc, "ρ(k) = Corr(r(t), r(t−k)) = 0,  với mọi k ≥ 1")
    para(doc,
         "Hệ quả phương pháp luận của giả thuyết này rất quan trọng đối với đề "
         "tài. Vì các chỉ báo kỹ thuật đều là hàm số của chuỗi giá quá khứ, giả "
         "thuyết hiệu quả dạng yếu dự đoán rằng chúng không có năng lực dự báo. "
         "Do đó độ lớn của hệ số tự tương quan chính là thước đo trực tiếp mức "
         "độ không hiệu quả của thị trường, và cũng là căn cứ để đề tài đưa nhóm "
         "đặc trưng trễ vào mô hình – vừa với vai trò biến dự báo, vừa với vai "
         "trò kiểm định giả thuyết.")

    heading(doc, "1.1.2. Giả thuyết Thị trường Thích nghi", level=3)
    para(doc,
         "Lo (2004) lập luận rằng hiệu quả thị trường không phải trạng thái tĩnh "
         "mà biến đổi theo thời gian. Các cơ hội sinh lợi xuất hiện khi có bất "
         "cân xứng thông tin hoặc thiên lệch hành vi, bị khai thác dần, rồi biến "
         "mất khi đủ nhiều nhà đầu tư nhận ra. Về mặt toán học, điều này có "
         "nghĩa phân phối có điều kiện của nhãn theo đặc trưng là không dừng:")
    formula(doc, "P(y | X) thay đổi theo thời gian t",
            note="Hiện tượng này được gọi là trôi khái niệm (concept drift).")
    para(doc,
         "Hàm ý phương pháp luận là mô hình dự báo phải được tái huấn luyện định "
         "kỳ thay vì huấn luyện một lần duy nhất. Đây chính là cơ sở của thiết "
         "kế walk-forward có chu kỳ tái huấn luyện được trình bày ở mục 2.5.")

    heading(doc, "1.1.3. Cơ sở lý thuyết của phân tích kỹ thuật", level=3)
    para(doc,
         "Phân tích kỹ thuật dựa trên ba tiền đề của Lý thuyết Dow, được hệ "
         "thống hóa bởi Murphy (1999). Thứ nhất, giá phản ánh mọi thông tin và "
         "tâm lý thị trường. Thứ hai, giá vận động theo xu hướng có quán tính – "
         "đây là cơ sở của nhóm chỉ báo xu hướng. Thứ ba, lịch sử có tính lặp "
         "lại do tâm lý nhà đầu tư lặp lại – đây là cơ sở của nhóm chỉ báo dao "
         "động.")
    para(doc,
         "Trong thực tiễn tồn tại hai trường phái đối lập cùng dựa trên các tiền "
         "đề này. Trường phái theo xu hướng (trend-following) giả định giá đang "
         "tăng sẽ tiếp tục tăng, khai thác quán tính, với các chỉ báo tiêu biểu "
         "là giao cắt trung bình động và MACD. Trường phái hồi quy về trung bình "
         "(mean-reversion) giả định giá bị đẩy quá xa giá trị trung bình sẽ quay "
         "trở lại, khai thác phản ứng thái quá của thị trường, với chỉ báo tiêu "
         "biểu là RSI và dải Bollinger.")
    para(doc,
         "Việc hai trường phái này đưa ra tín hiệu trái ngược nhau trong cùng "
         "một tình huống thị trường là lý do đề tài lựa chọn benchmark từ cả hai "
         "trường phái. Nếu chỉ so sánh chiến lược trí tuệ nhân tạo với "
         "trend-following, kết luận sẽ phụ thuộc vào việc giai đoạn kiểm định có "
         "xu hướng rõ ràng hay không, dẫn tới thiên lệch.")

    # ---------------------------------------------------------------- 1.2
    heading(doc, "1.2. Cơ sở lựa chọn dạng bài toán và biến mục tiêu", level=2)

    heading(doc, "1.2.1. Log-return và các tính chất", level=3)
    para(doc, "Lợi suất logarit của ngày t được định nghĩa:")
    formula(doc, "r(t) = ln( P(t) / P(t−1) )",
            note="Trong đó P(t) là giá đóng cửa ngày t.")
    para(doc,
         "Đề tài sử dụng log-return thay vì chênh lệch giá tuyệt đối vì ba lý "
         "do. Thứ nhất là tính cộng dồn theo thời gian: lợi suất nhiều kỳ bằng "
         "tổng lợi suất từng kỳ, do đó khi tính đường giá trị tài sản của chiến "
         "lược ta chỉ cần cộng dồn thay vì nhân dồn:")
    formula(doc, "r(t → t+k) = r(t+1) + r(t+2) + … + r(t+k)")
    para(doc,
         "Thứ hai là ổn định phương sai. Giá vàng trong giai đoạn nghiên cứu đi "
         "từ khoảng 1.200 lên khoảng 4.000 đơn vị. Nếu dùng chênh lệch tuyệt "
         "đối, một biến động 1% năm 2015 tương ứng 12 đơn vị giá còn năm 2025 "
         "tương ứng 40 đơn vị, khiến phương sai tăng theo mức giá và vi phạm giả "
         "định đồng nhất phương sai. Thứ ba là tính đối xứng: giá tăng gấp đôi "
         "cho r = ln2 = +0,693 còn giá giảm một nửa cho r = −0,693, hai giá trị "
         "đối xứng hoàn hảo, trong khi với lợi suất số học là +100% và −50%.")

    heading(doc, "1.2.2. Cơ sở của lựa chọn phân loại nhị phân", level=3)
    para(doc, "Biến mục tiêu được định nghĩa:")
    formula(doc, "y(t) = 1 nếu r(t+1) > 0;   y(t) = 0 nếu r(t+1) ≤ 0")
    para(doc,
         "Lựa chọn phân loại nhị phân thay vì hồi quy giá trị lợi suất xuất phát "
         "từ hàm mục tiêu của người ra quyết định. Quyết định giao dịch Long hay "
         "Flat chỉ phụ thuộc dấu của lợi nhuận kỳ vọng, không phụ thuộc độ lớn. "
         "Nếu dùng hồi quy, hàm mất mát là sai số bình phương trung bình:")
    formula(doc, "MSE = (1/N) · Σ ( r_thực − r_dự_báo )²")
    para(doc,
         "Vì sai số được bình phương, một quan sát sai 5% đóng góp vào MSE gấp "
         "25 lần quan sát sai 1%. Do đó mô hình hồi quy sẽ dành phần lớn năng "
         "lực để dự báo đúng các cú biến động lớn, trong khi mục tiêu giao dịch "
         "là dự báo đúng hướng ở đa số phiên. Hai hàm mục tiêu này không đồng "
         "nhất, nên tối ưu hóa MSE không tối ưu hóa hiệu quả giao dịch.")

    # ---------------------------------------------------------------- 1.3
    heading(doc, "1.3. Thuật toán XGBoost", level=2)

    heading(doc, "1.3.1. Mô hình tổng thể và cơ chế boosting", level=3)
    para(doc,
         "XGBoost (Chen và Guestrin, 2016) là thuật toán tăng cường gradient "
         "trên cây quyết định. Dự báo cuối cùng là tổng đóng góp của M cây:")
    formula(doc, "F(x) = F₀ + η · [ f₁(x) + f₂(x) + … + f_M(x) ]",
            note="F₀ là giá trị khởi tạo, η là learning rate, f_m là cây thứ m.")
    para(doc,
         "Điểm khác biệt cốt lõi so với rừng ngẫu nhiên là các cây được xây tuần "
         "tự thay vì song song: mỗi cây mới được xây để sửa lỗi của tổ hợp các "
         "cây trước đó. Đây là ý nghĩa của khái niệm boosting.")

    heading(doc, "1.3.2. Hàm mất mát và hàm mục tiêu có điều chuẩn", level=3)
    para(doc,
         "Với bài toán phân loại nhị phân, hàm mất mát là log-loss:")
    formula(doc, "l(y, p) = − [ y · ln(p) + (1 − y) · ln(1 − p) ]")
    para(doc,
         "Hàm này phạt rất nặng những dự báo sai mà tự tin: nếu y = 1 và p tiến "
         "về 0 thì mất mát tiến ra vô cùng. Đặc tính này buộc mô hình phải trung "
         "thực về mức độ không chắc chắn của mình, là cơ sở để đầu ra xác suất "
         "có thể diễn giải được. Hàm mục tiêu tổng thể bổ sung thành phần điều "
         "chuẩn phạt độ phức tạp của cây:")
    formula(doc, "Obj = Σᵢ l(yᵢ, pᵢ) + Σₘ Ω(fₘ),   với  Ω(f) = γ·T + (½)·λ·Σⱼ wⱼ²",
            note="T là số lá, wⱼ là trọng số lá j, γ là chi phí mỗi lá, "
                 "λ là hệ số điều chuẩn L2.")
    para(doc,
         "Việc đưa điều chuẩn trực tiếp vào hàm mục tiêu thay vì xử lý sau bằng "
         "cắt tỉa là một điểm khác biệt của XGBoost so với tăng cường gradient "
         "truyền thống, và đặc biệt có giá trị với dữ liệu tài chính vốn có tỷ lệ "
         "tín hiệu trên nhiễu thấp.")

    heading(doc, "1.3.3. Xấp xỉ Taylor bậc hai", level=3)
    para(doc,
         "Tại vòng lặp thứ m, hàm mục tiêu được khai triển Taylor bậc hai quanh "
         "dự báo hiện tại:")
    formula(doc, "Objₘ ≈ Σᵢ [ gᵢ · fₘ(xᵢ) + (½) · hᵢ · fₘ(xᵢ)² ] + Ω(fₘ)")
    para(doc,
         "trong đó g là đạo hàm bậc nhất (gradient) và h là đạo hàm bậc hai "
         "(Hessian) của hàm mất mát theo điểm số dự báo. Với log-loss kết hợp "
         "liên kết sigmoid, hai đại lượng này có dạng đóng rất đơn giản:")
    formula(doc, "gᵢ = pᵢ − yᵢ  ;   hᵢ = pᵢ · (1 − pᵢ)")
    para(doc,
         "Gradient chính là sai số dự báo, nên mỗi cây mới học trực tiếp phần sai "
         "số còn lại. Hessian đạt cực đại 0,25 khi p = 0,5 và tiến về không khi "
         "p tiến về 0 hoặc 1, nghĩa là những quan sát mà mô hình còn chưa chắc "
         "chắn được coi là chứa nhiều thông tin để học, còn những quan sát đã "
         "chắc chắn gần như bị bỏ qua ở các vòng sau. Việc sử dụng cả đạo hàm "
         "bậc hai cho phép xác định bước nhảy tối ưu chính xác hơn so với chỉ "
         "dùng gradient.")

    heading(doc, "1.3.4. Trọng số lá tối ưu và công thức Gain", level=3)
    para(doc,
         "Ký hiệu G và H là tổng gradient và tổng Hessian của các quan sát rơi "
         "vào một lá. Tối thiểu hóa hàm mục tiêu bậc hai theo trọng số lá cho "
         "nghiệm:")
    formula(doc, "w* = − G / ( H + λ )")
    para(doc,
         "Vì λ nằm ở mẫu số, hệ số điều chuẩn càng lớn thì trọng số lá càng bị "
         "co về không, ngăn các lá có ít mẫu tạo ra dự báo cực đoan. Tiêu chí "
         "chọn điểm chia là mức giảm hàm mất mát nhờ phép chia:")
    formula(doc,
            "Gain = (½) · [ G_L²/(H_L+λ) + G_R²/(H_R+λ) − (G_L+G_R)²/(H_L+H_R+λ) ] − γ")
    para(doc,
         "Tại mỗi node, thuật toán duyệt qua toàn bộ các đặc trưng và các ngưỡng "
         "chia khả thi, tính Gain cho từng cặp và chọn cặp có Gain lớn nhất. Do "
         "đó công thức này chính là cơ chế quyết định đặc trưng nào được sử dụng "
         "và ở vị trí nào trong cây, và là nền tảng của chỉ số độ quan trọng đặc "
         "trưng dạng Gain được phân tích ở mục 3.3.")

    heading(doc, "1.3.5. Chuyển điểm số thành xác suất", level=3)
    para(doc,
         "Đầu ra trực tiếp của XGBoost là điểm số thô F(x), một số thực không "
         "giới hạn. Để chuyển thành xác suất, thuật toán áp dụng hàm sigmoid:")
    formula(doc, "P(giá tăng) = 1 / ( 1 + e^(−F(x)) )")
    para(doc,
         "Hàm sigmoid ánh xạ toàn bộ trục số thực vào khoảng (0, 1) và đối xứng "
         "quanh điểm F = 0, p = 0,5. Quan hệ nghịch là hàm logit, F = ln[p/(1−p)], "
         "nên có thể nói XGBoost dự báo log-odds rồi sigmoid chuyển log-odds "
         "thành xác suất. Đặc điểm này quan trọng vì đầu ra xác suất cho phép "
         "xây dựng bộ lọc theo mức độ tin cậy, được khai thác trong chiến lược "
         "trình bày ở mục 2.6.")

    # ---------------------------------------------------------------- 1.4
    heading(doc, "1.4. Hệ chỉ tiêu đánh giá hiệu quả chiến lược", level=2)
    para(doc,
         "Đề tài sử dụng đồng thời nhiều chỉ tiêu vì không một chỉ tiêu đơn lẻ "
         "nào đủ để mô tả hiệu quả chiến lược: một chiến lược có thể đạt tỷ số "
         "Sharpe cao nhưng có mức sụt giảm không thể chấp nhận về mặt tâm lý.")

    heading(doc, "1.4.1. Nhóm chỉ tiêu lợi nhuận", level=3)
    para(doc, "Tổng lợi nhuận toàn kỳ và tốc độ tăng trưởng kép hàng năm:")
    formula(doc, "TotalReturn = E(n) − 1   ;   CAGR = [ E(n) ]^(P/n) − 1",
            note="E(n) là giá trị tài sản cuối kỳ (khởi điểm 1,0), n là số quan "
                 "sát, P là số quan sát mỗi năm.")

    heading(doc, "1.4.2. Nhóm chỉ tiêu rủi ro", level=3)
    para(doc, "Độ biến động hàng năm và mức sụt giảm tối đa:")
    formula(doc, "AnnVol = std(s) · √P")
    formula(doc, "MaxDD = min over t của [ E(t) / max{E(1),…,E(t)} − 1 ]")
    para(doc,
         "Hệ số √P xuất phát từ quy tắc căn bậc hai của thời gian: nếu các lợi "
         "suất hàng ngày độc lập thì phương sai cộng dồn theo thời gian, do đó "
         "độ lệch chuẩn nhân với căn của số kỳ. Mức sụt giảm tối đa có ý nghĩa "
         "đặc biệt vì đây là thước đo rủi ro dưới dạng trải nghiệm – nó quyết "
         "định khả năng nhà giao dịch trụ lại với chiến lược trong thực tế, điều "
         "mà độ lệch chuẩn không phản ánh được. Hai chiến lược có cùng độ lệch "
         "chuẩn có thể có mức sụt giảm tối đa rất khác nhau.")

    heading(doc, "1.4.3. Nhóm chỉ tiêu hiệu quả điều chỉnh rủi ro", level=3)
    formula(doc, "Sharpe = [ mean(s) / std(s) ] · √P")
    formula(doc, "Sortino = [ mean(s) / DownsideStd ] · √P")
    formula(doc, "Calmar = CAGR / | MaxDD |")
    para(doc,
         "Tỷ số Sharpe (Sharpe, 1966) đo lợi nhuận trên một đơn vị rủi ro tổng "
         "và là thước đo phổ biến nhất, nhưng có hai hạn chế cần lưu ý: nó phạt "
         "cả biến động tăng – điều mà nhà đầu tư không coi là rủi ro – và giả "
         "định lợi suất xấp xỉ phân phối chuẩn trong khi lợi suất tài chính có "
         "đuôi dày. Tỷ số Sortino (Sortino và Price, 1994) khắc phục hạn chế thứ "
         "nhất bằng cách chỉ tính độ lệch chuẩn của các lợi suất âm. Do đó khi "
         "Sortino thấp hơn Sharpe đáng kể, đó là dấu hiệu tỷ số Sharpe cao chủ "
         "yếu nhờ độ lệch chuẩn tổng nhỏ chứ không nhờ phân bố lợi nhuận thuận "
         "lợi – một nhận xét sẽ được sử dụng khi diễn giải kết quả ở Chương 3.")

    heading(doc, "1.4.4. Nhóm chỉ tiêu tính ổn định", level=3)
    para(doc,
         "Tính ổn định là tiêu chí thứ ba trong mục tiêu đề tài. Cơ sở lý luận "
         "là một chiến lược có thể đạt Sharpe cao toàn kỳ nhờ một vài giai đoạn "
         "bất thường trong khi thua lỗ ở các giai đoạn khác. Đề tài đo tính ổn "
         "định bằng ba chỉ tiêu bổ trợ: lợi nhuận từng năm, độ lệch chuẩn của "
         "chuỗi lợi nhuận năm, và tỷ lệ số năm có lãi kèm mức lợi nhuận của năm "
         "xấu nhất. Ba chỉ tiêu này phải được đọc đồng thời, vì một chiến lược "
         "có độ lệch chuẩn nhỏ nhưng tỷ lệ năm có lãi thấp là chiến lược ổn định "
         "trong việc không sinh lợi.")


def chuong_2(doc):
    heading(doc, "CHƯƠNG 2. DỮ LIỆU VÀ PHƯƠNG PHÁP NGHIÊN CỨU",
            level=1, align="center", page_break=True)

    # ---------------------------------------------------------------- 2.1
    heading(doc, "2.1. Mô tả dữ liệu", level=2)
    para(doc,
         "Dữ liệu sử dụng trong nghiên cứu là chuỗi giá vàng theo ngày giai đoạn "
         "02/01/2015 – 30/12/2025, gồm 4.016 quan sát với bảy trường dữ liệu: "
         "ngày, giá mở cửa, giá cao nhất, giá thấp nhất, giá đóng cửa, khối "
         "lượng giao dịch và hợp đồng mở. Dữ liệu không có giá trị khuyết ở bất "
         "kỳ trường nào và toàn bộ các dòng đều thỏa mãn ràng buộc logic của bộ "
         "giá OHLC.")

    table(doc,
          caption_title="Thống kê mô tả bộ dữ liệu nghiên cứu",
          headers=["Chỉ tiêu", "Giá trị"],
          rows=[
              ["Số quan sát", "4.016"],
              ["Khoảng thời gian", "02/01/2015 – 30/12/2025"],
              ["Số quan sát mỗi năm", "≈ 365"],
              ["Giá đóng cửa nhỏ nhất", "≈ 1.054"],
              ["Giá đóng cửa lớn nhất", "≈ 4.498"],
              ["Tỷ lệ ngày tăng giá", "66,13%"],
              ["Giá trị khuyết", "Không có"],
          ],
          widths=[3.2, 2.2],
          note="Nguồn: tính toán của nhóm nghiên cứu từ bộ dữ liệu đề tài.")

    # ---------------------------------------------------------------- 2.2
    heading(doc, "2.2. Kiểm định chất lượng dữ liệu", level=2)
    para(doc,
         "Trước khi diễn giải bất kỳ kết quả dự báo nào, đề tài thực hiện kiểm "
         "định để xác định cấu trúc dự báo có nguồn gốc từ thị trường hay từ quy "
         "trình xử lý dữ liệu. Bước này là cần thiết vì việc bỏ qua nó là nguyên "
         "nhân phổ biến nhất của các kết quả nghiên cứu không thể tái lập trong "
         "tài chính định lượng. Ba phép kiểm định được sử dụng, mỗi phép dựa trên "
         "một đặc tính thống kê đã được xác lập của chuỗi giá tài chính thực.")

    heading(doc, "2.2.1. Ba phép kiểm định và cơ sở lý luận", level=3)
    bullet(doc, "Chuỗi giá thật gần như không bao giờ có hai bước nhảy liên tiếp "
                "bằng nhau tuyệt đối, vì giá do hàng triệu giao dịch độc lập tạo "
                "thành. Tỷ lệ trùng cao là dấu hiệu của phép nội suy.",
           bold_prefix="Tỷ lệ bước giá trùng lặp: ")
    bullet(doc, "Theo giả thuyết hiệu quả dạng yếu, thị trường thanh khoản cao "
                "có hệ số tự tương quan bậc một nhỏ hơn 0,05 về giá trị tuyệt đối.",
           bold_prefix="Tự tương quan log-return: ")
    bullet(doc, "Hợp đồng vàng tương lai trên sàn COMEX không giao dịch Thứ Bảy "
                "và Chủ Nhật, nên dữ liệu thật không thể có quan sát vào hai "
                "ngày này.",
           bold_prefix="Phân bố ngày trong tuần: ")

    heading(doc, "2.2.2. Kết quả kiểm định", level=3)
    table(doc,
          caption_title="Kết quả kiểm định chất lượng dữ liệu",
          headers=["Phép kiểm định", "Ngưỡng kỳ vọng\n(dữ liệu thật)",
                   "Kết quả thực tế"],
          rows=[
              ["Tỷ lệ bước giá trùng bước trước", "≈ 0%", "**76,07%**"],
              ["Tự tương quan log-return bậc 1", "|ρ| < 0,05", "0,0415"],
              ["Tự tương quan log-return bậc 2", "|ρ| < 0,05", "0,0675"],
              ["Số quan sát vào Thứ Bảy và Chủ Nhật", "0", "**1.148**"],
              ["Tỷ lệ ngày tăng giá", "52 – 53%", "**66,13%**"],
              ["Khoảng cách giữa các quan sát", "Có gap cuối tuần",
               "100% = 1 ngày"],
          ],
          widths=[3.6, 2.2, 2.0],
          note="Nguồn: kết quả chạy chương trình check_data_quality.py.")

    para(doc,
         "Phân bố quan sát theo ngày trong tuần cho thấy dữ liệu có đủ bảy ngày "
         "mỗi tuần với số lượng gần bằng nhau: Thứ Hai 574, Thứ Ba 574, Thứ Tư "
         "573, Thứ Năm 573, Thứ Sáu 574, Thứ Bảy 574 và Chủ Nhật 574 quan sát. "
         "Do thị trường vàng không giao dịch cuối tuần, sự hiện diện của 1.148 "
         "quan sát vào Thứ Bảy và Chủ Nhật là bằng chứng cho thấy các ngày không "
         "giao dịch đã được điền giá trị.")

    heading(doc, "2.2.3. Chứng minh hiện tượng nội suy", level=3)
    para(doc,
         "Kiểm tra bốn quan sát đầu tiên của bộ dữ liệu cho thấy rõ bản chất của "
         "phép điền giá trị này.")

    table(doc,
          caption_title="Minh chứng hiện tượng nội suy tuyến tính "
                        "trong bốn quan sát đầu",
          headers=["Ngày", "Thứ", "Giá đóng cửa", "Bước nhảy"],
          rows=[
              ["02/01/2015", "Sáu", "1.186,000", "—"],
              ["03/01/2015", "**Bảy**", "1.191,967", "+5,966675"],
              ["04/01/2015", "**Chủ Nhật**", "1.197,933", "+5,966675"],
              ["05/01/2015", "Hai", "1.203,900", "+5,966675"],
          ],
          widths=[1.8, 1.6, 2.0, 1.8],
          note="Nguồn: bộ dữ liệu đề tài.")

    para(doc,
         "Ba bước nhảy liên tiếp bằng nhau tuyệt đối đến sáu chữ số thập phân. "
         "Kiểm chứng bằng công thức nội suy tuyến tính: với giá Thứ Sáu là "
         "1.186,000, giá Thứ Hai là 1.203,900 và ba bước ở giữa, mỗi bước bằng "
         "(1.203,900 − 1.186,000) / 3 = 5,966667 – khớp với giá trị quan sát "
         "được. Trường hợp thứ hai là các ngày 17, 18 và 19/01/2015 (Thứ Bảy, "
         "Chủ Nhật và Thứ Hai là ngày lễ Martin Luther King, thị trường Mỹ đóng "
         "cửa) đều có bước nhảy bằng +4,324982. Như vậy giá các ngày không giao "
         "dịch được điền bằng nội suy tuyến tính giữa hai ngày giao dịch liền kề.")

    heading(doc, "2.2.4. Hệ quả về mặt phương pháp luận", level=3)
    para(doc,
         "Giá ngày Thứ Bảy và Chủ Nhật được suy ra từ giá ngày Thứ Hai kế sau:")
    formula(doc, "P(Thứ Bảy) = P(Thứ Sáu) + [ P(Thứ Hai) − P(Thứ Sáu) ] / 3")
    para(doc,
         "Nghĩa là giá trị tại thời điểm t được tính từ thông tin chưa tồn tại "
         "tại thời điểm đó – đây chính là định nghĩa của rò rỉ thông tin tương "
         "lai (look-ahead leakage). Hệ quả đối với mô hình là trong các đoạn nội "
         "suy, quan hệ r(t+1) = r(t) đúng một cách xác định, do đó mô hình chỉ "
         "cần nhận diện quan sát đang nằm trong đoạn nội suy là đã dự báo đúng "
         "gần như hoàn toàn. Đây là năng lực không tồn tại trên thị trường thực.")
    para(doc,
         "Nhận định này cũng giải thích vì sao tỷ lệ ngày tăng giá đạt 66,13% "
         "thay vì khoảng 53% như dữ liệu thật: mỗi lần giá tăng qua cuối tuần, "
         "phép nội suy tạo ra ba ngày tăng liên tiếp thay vì một. Kết quả nghiên "
         "cứu ở Chương 3 vì vậy được trình bày kèm thí nghiệm đối chứng ở mục "
         "3.7 và phần đánh giá hạn chế ở mục 4.5.1.")

    # ---------------------------------------------------------------- 2.3
    heading(doc, "2.3. Xây dựng tập đặc trưng", level=2)
    para(doc,
         "Tập đặc trưng gồm 14 biến thuộc bốn nhóm, được thiết kế để bao phủ bốn "
         "chiều thông tin độc lập của chuỗi giá.")

    heading(doc, "2.3.1. Nguyên tắc chuẩn hóa", level=3)
    para(doc,
         "Đây là quyết định thiết kế quan trọng nhất của quá trình xây dựng đặc "
         "trưng. Vấn đề là cây quyết định phân chia không gian bằng ngưỡng tuyệt "
         "đối dạng “nếu MA10 nhỏ hơn c”. Vì mức giá vàng năm 2015 khoảng 1.200 "
         "còn năm 2025 khoảng 4.000, ngưỡng c học được từ dữ liệu 2015 – 2019 "
         "trở nên vô nghĩa khi áp dụng cho 2020 – 2025. Giải pháp là đưa vào mô "
         "hình các đại lượng bất biến theo mức giá, tức tỷ lệ phần trăm thay vì "
         "giá trị tuyệt đối.")
    para(doc,
         "Việc chuẩn hóa còn mang lại lợi ích thứ hai là cung cấp sẵn quan hệ "
         "tương tác. Chênh lệch MA ngắn trừ MA dài chính là định nghĩa toán học "
         "của tín hiệu giao cắt. Nếu chỉ đưa vào MA10 và MA30 riêng lẻ, cây "
         "quyết định phải xấp xỉ mặt phân chia chéo MA10 − MA30 = 0 bằng nhiều "
         "lần chia trực giao liên tiếp, tạo thành một chuỗi bậc thang cần hàng "
         "chục node – rất kém hiệu quả về mặt thống kê. Với biến chênh lệch, mô "
         "hình chỉ cần một lần chia tại ngưỡng không.")

    heading(doc, "2.3.2. Nhóm 1 – Chỉ báo xu hướng", level=3)
    formula(doc, "MA(n)(t) = [ P(t) + P(t−1) + … + P(t−n+1) ] / n")
    formula(doc, "EMA(n)(t) = α · P(t) + (1 − α) · EMA(n)(t−1),   α = 2/(n+1)")
    para(doc,
         "Trung bình động là bộ lọc thông thấp, triệt tiêu dao động tần số cao "
         "và giữ lại thành phần xu hướng. Trung bình động hàm mũ gán trọng số suy "
         "giảm theo hàm mũ khi lùi về quá khứ, nên phản ứng nhanh hơn khi thị "
         "trường đổi chế độ. Đề tài chọn ba khung 10, 30 và 50 kỳ để bao phủ xu "
         "hướng ngắn, trung và dài hạn, cùng cặp 12 và 26 kỳ là tham số chuẩn của "
         "MACD. Bốn đặc trưng thực tế đưa vào mô hình đều ở dạng chuẩn hóa:")
    bullet(doc, "(MA10 − MA30) / MA30", bold_prefix="MA10_MA30_diff = ")
    bullet(doc, "(MA30 − MA50) / MA50", bold_prefix="MA30_MA50_diff = ")
    bullet(doc, "(EMA12 − EMA26) / EMA26", bold_prefix="EMA12_EMA26_diff = ")
    bullet(doc, "(P − MA10) / MA10", bold_prefix="price_MA10_dist = ")

    heading(doc, "2.3.3. Nhóm 2 – Chỉ báo động lượng và dao động", level=3)
    para(doc, "Chỉ số sức mạnh tương đối (Wilder, 1978) được tính qua bốn bước:")
    formula(doc, "RS = AvgGain(14) / AvgLoss(14)   ;   RSI = 100 − 100/(1 + RS)")
    para(doc,
         "RSI có thang đo cố định trong khoảng 0 đến 100, không phụ thuộc mức giá "
         "và không phụ thuộc thời gian. Đây là ưu điểm đặc biệt với mô hình cây: "
         "ngưỡng chia mà cây học được vẫn giữ nguyên hiệu lực ở tương lai, khác "
         "với các biến dựa trên mức giá. Đường phân kỳ hội tụ trung bình động "
         "(Appel, 1979) đo khoảng cách hai trung bình động hàm mũ:")
    formula(doc, "MACD = EMA12 − EMA26  ;  Signal = EMA9(MACD)  ;  "
                 "Hist = MACD − Signal")
    para(doc,
         "MACD biểu diễn gia tốc của xu hướng, còn histogram tương ứng đạo hàm "
         "bậc hai của giá nên có khả năng phát hiện phân kỳ trước khi giá đảo "
         "chiều. Vì MACD nguyên bản có đơn vị là đơn vị giá – biên độ dao động "
         "khoảng ±15 năm 2015 nhưng ±50 năm 2025 – đề tài chuẩn hóa theo giá "
         "trước khi đưa vào mô hình, tạo thành hai đặc trưng MACD_norm = MACD/P "
         "và MACD_hist_norm = Hist/P.")

    heading(doc, "2.3.4. Nhóm 3 – Chỉ báo độ biến động", level=3)
    para(doc,
         "Dải Bollinger được xây dựng từ trung bình động 20 kỳ và độ lệch chuẩn "
         "20 kỳ của giá, với hệ số 2 xuất phát từ tính chất phân phối chuẩn "
         "(khoảng ±2 độ lệch chuẩn chứa khoảng 95,4% quan sát). Hai đặc trưng "
         "dẫn xuất:")
    formula(doc, "BB_width = 4·σ(20) / MA20")
    formula(doc, "BB_pctB = [ P − (MA20 − 2σ) ] / (4σ) = (z + 2) / 4",
            note="z là z-score của giá so với trung bình 20 kỳ.")
    para(doc,
         "Phép biến đổi cho thấy BB_pctB thực chất là z-score chuẩn hóa – đo mức "
         "độ lệch của giá khỏi trung bình theo đơn vị độ lệch chuẩn, bất biến "
         "theo cả mức giá và mức biến động. Hai đặc trưng còn lại là độ biến động "
         "20 ngày (độ lệch chuẩn của log-return) và tỷ lệ khối lượng so với trung "
         "bình trượt 20 kỳ.")
    para(doc,
         "Cơ sở thống kê cho tính dự báo của nhóm này là hiện tượng tụ cụm biến "
         "động do Mandelbrot (1963) phát hiện và Engle (1982) mô hình hóa: biến "
         "động cao có xu hướng theo sau biến động cao. Khác với chuỗi lợi suất "
         "gần như ngẫu nhiên, chuỗi biến động có tự tương quan dương và bền vững, "
         "nên là biến có tính dự báo ổn định.")
    para(doc,
         "Điều quan trọng hơn là lý luận về chế độ thị trường. Quan hệ giữa chỉ "
         "báo và hướng giá không ổn định mà phụ thuộc trạng thái biến động: cùng "
         "một tín hiệu MACD dương mang ý nghĩa khác nhau trong chế độ biến động "
         "thấp (xu hướng bền) so với chế độ biến động cao (nhiễu lớn, dễ đảo "
         "chiều). Vì cây quyết định phân chia không gian đặc trưng thành các vùng "
         "rời rạc rồi học quy tắc riêng cho từng vùng, việc cung cấp biến biến "
         "động cho phép mô hình học quy tắc có điều kiện theo chế độ. Đây chính "
         "là loại tương tác phi tuyến mà mô hình tuyến tính không thể biểu diễn "
         "nếu không tạo biến tương tác thủ công, và do đó là cơ sở lý luận cho "
         "việc lựa chọn XGBoost thay vì hồi quy logistic.")

    heading(doc, "2.3.5. Nhóm 4 – Đặc trưng trễ", level=3)
    para(doc,
         "Ba biến log-return trễ một, hai và ba ngày nắm bắt cấu trúc tự tương "
         "quan bậc thấp của chuỗi lợi suất – thành phần thông tin mà bốn nhóm "
         "trên không biểu diễn được, do các biến đó đều là kết quả của phép trung "
         "bình nên đã mất thông tin về từng bước nhảy riêng lẻ. Theo giả thuyết "
         "hiệu quả dạng yếu, nhóm này lẽ ra không có năng lực dự báo, nên độ lớn "
         "đóng góp của nó là thước đo định lượng mức độ không hiệu quả của thị "
         "trường. Tuy nhiên, kết quả kiểm định ở mục 2.2 cho thấy cần thận trọng "
         "khi diễn giải đóng góp của nhóm này trên bộ dữ liệu hiện có.")

    table(doc,
          caption_title="Tổng hợp tập đặc trưng đưa vào mô hình",
          headers=["Nhóm", "Số biến", "Tên biến"],
          rows=[
              ["Nhóm 1 – Xu hướng", "4",
               "MA10_MA30_diff, MA30_MA50_diff, EMA12_EMA26_diff, price_MA10_dist"],
              ["Nhóm 2 – Động lượng", "3", "RSI14, MACD_norm, MACD_hist_norm"],
              ["Nhóm 3 – Biến động", "4",
               "BB_width, BB_pctB, volatility_20d, volume_ratio"],
              ["Nhóm 4 – Đặc trưng trễ", "3",
               "log_return_lag1, log_return_lag2, log_return_lag3"],
              ["**Tổng**", "**14**", ""],
          ],
          widths=[2.2, 1.0, 4.8],
          note="Nguồn: thiết kế của nhóm nghiên cứu.")

    heading(doc, "2.3.6. Xử lý giá trị khuyết", level=3)
    para(doc,
         "Các đặc trưng sử dụng cửa sổ trượt tạo ra giá trị khuyết ở đầu chuỗi, "
         "với cửa sổ dài nhất là 50 kỳ. Đề tài cắt bỏ các quan sát không đầy đủ "
         "thay vì dùng phép thay thế, vì với chuỗi thời gian ở vùng khởi động mọi "
         "giá trị thay thế đều là thông tin bị bóp méo: điền bằng giá trị trung "
         "bình sẽ đưa vào thông tin của toàn chuỗi kể cả tương lai, còn điền "
         "ngược cũng dùng thông tin tương lai. Tổn thất 49 quan sát trên 4.016 "
         "tương ứng 1,2% là không đáng kể. Quan sát cuối cùng cũng bị loại vì "
         "không xác định được nhãn.")

    # ---------------------------------------------------------------- 2.4
    heading(doc, "2.4. Quy ước chống rò rỉ thông tin", level=2)
    para(doc,
         "Vì nhãn tại thời điểm t mô tả tương lai t+1, mọi đặc trưng tại t chỉ "
         "được tính từ thông tin đến hết ngày t. Điều này được thực thi bằng ba "
         "cơ chế: mọi cửa sổ trượt đều là cửa sổ đóng lùi về quá khứ; thiết kế "
         "walk-forward ở mục 2.5; và quy ước thực thi giao dịch ở mục 2.6.")

    # ---------------------------------------------------------------- 2.5
    heading(doc, "2.5. Thiết kế kiểm định walk-forward", level=2)

    heading(doc, "2.5.1. Cơ sở loại trừ kiểm định chéo ngẫu nhiên", level=3)
    para(doc,
         "Kiểm định chéo K-Fold ngẫu nhiên giả định các quan sát độc lập và cùng "
         "phân phối – giả định bị vi phạm hoàn toàn với chuỗi thời gian. Hai vấn "
         "đề cụ thể phát sinh. Thứ nhất, khi trộn ngẫu nhiên, tập huấn luyện "
         "chứa các quan sát xảy ra sau tập kiểm định, khiến mô hình học từ tương "
         "lai để dự báo quá khứ và kết quả bị phóng đại một cách hệ thống. Thứ "
         "hai, các quan sát gần nhau về thời gian có tương quan cao – đặc trưng "
         "MA50 tại ngày t và t+1 chia sẻ 49 trong 50 giá trị – nên nếu hai ngày "
         "liền kề bị chia vào tập huấn luyện và tập kiểm định thì hai tập gần như "
         "trùng lặp thông tin, làm ước lượng sai số quá lạc quan.")

    heading(doc, "2.5.2. Thiết kế cửa sổ mở rộng", level=3)
    formula(doc, "Huấn luyện [0, t) → Dự báo [t, t+h) → t := t + h")
    para(doc,
         "Đề tài sử dụng tập huấn luyện ban đầu 1.825 quan sát tương ứng khoảng "
         "năm năm, và chu kỳ tái huấn luyện h = 365 quan sát tương ứng khoảng "
         "một năm. Kết quả là chuỗi ngoài mẫu liên tục từ 19/02/2020 đến "
         "29/12/2025 gồm 2.141 quan sát.")
    para(doc,
         "Thiết kế này được lựa chọn vì ba lý do. Một là mô phỏng đúng điều kiện "
         "thực tế: tại mọi thời điểm ra quyết định, nhà giao dịch chỉ có dữ liệu "
         "quá khứ. Hai là thích nghi với trôi khái niệm, trực tiếp hiện thực hóa "
         "hàm ý của Giả thuyết Thị trường Thích nghi trình bày ở mục 1.1.2. Ba là "
         "tạo ra chuỗi ngoài mẫu dài liên tục, điều kiện cần để tính được đường "
         "giá trị tài sản, mức sụt giảm tối đa và lợi nhuận theo từng năm.")
    para(doc,
         "Đề tài chọn cửa sổ mở rộng thay vì cửa sổ trượt có độ dài cố định. "
         "Đánh đổi giữa hai phương án là cửa sổ mở rộng có nhiều dữ liệu hơn nên "
         "phương sai ước lượng thấp hơn nhưng chậm thích nghi với chế độ mới, "
         "còn cửa sổ trượt thì ngược lại. Với chuỗi chỉ 11 năm, cửa sổ mở rộng "
         "được ưu tiên để bảo đảm đủ dữ liệu huấn luyện.")

    heading(doc, "2.5.3. Cơ sở lựa chọn siêu tham số", level=3)
    table(doc,
          caption_title="Siêu tham số mô hình XGBoost và cơ sở lựa chọn",
          headers=["Tham số", "Giá trị", "Cơ sở lý luận"],
          rows=[
              ["max_depth", "3",
               "Dữ liệu tài chính có tỷ lệ tín hiệu trên nhiễu thấp; cây sâu sẽ "
               "khớp nhiễu. Độ sâu 3 cho tối đa 8 lá, buộc mô hình học quy tắc "
               "tổng quát."],
              ["learning_rate", "0,05",
               "Mỗi cây đóng góp nhỏ nên mô hình tiến từng bước, hội tụ ổn định "
               "và giảm phương sai của tổ hợp."],
              ["n_estimators", "200",
               "Kết hợp với learning rate thấp để đủ năng lực học mà không quá "
               "khớp."],
              ["subsample", "0,8",
               "Mỗi cây dùng 80% quan sát, giảm tương quan giữa các cây."],
              ["colsample_bytree", "0,8",
               "Mỗi cây dùng 80% đặc trưng, ngăn một biến mạnh chi phối toàn bộ "
               "mô hình."],
              ["reg_lambda", "1,0",
               "Điều chuẩn L2 lên trọng số lá, hạn chế lá có giá trị cực trị do "
               "ít mẫu."],
              ["min_child_weight", "5",
               "Yêu cầu tổng Hessian tại lá tối thiểu 5; vì h ≤ 0,25 nên tương "
               "đương khoảng 20 quan sát mỗi lá."],
              ["scale_pos_weight", "n₋/n₊",
               "Xử lý mất cân bằng lớp, tránh mô hình suy biến thành luôn dự báo "
               "lớp đa số. Tính lại ở mỗi vòng tái huấn luyện."],
              ["random_state", "42", "Bảo đảm khả năng tái lập kết quả."],
          ],
          widths=[1.8, 1.0, 5.2],
          font_size=10,
          note="Nguồn: thiết kế của nhóm nghiên cứu.")

    para(doc,
         "Cần lưu ý rằng hệ số scale_pos_weight được tính lại ở mỗi vòng tái "
         "huấn luyện dựa trên tập huấn luyện tại thời điểm đó. Nếu tính một lần "
         "trên toàn chuỗi thì đã sử dụng thông tin tương lai, tạo thành một dạng "
         "rò rỉ tinh vi thường bị bỏ qua.")

    # ---------------------------------------------------------------- 2.6
    heading(doc, "2.6. Xây dựng chiến lược giao dịch", level=2)

    heading(doc, "2.6.1. Quy ước thực thi", level=3)
    para(doc,
         "Đây là quy ước quan trọng nhất bảo đảm tính trung thực của backtest. "
         "Tín hiệu tại ngày t được tính từ thông tin đến hết ngày t; vị thế được "
         "mở tại giá đóng cửa ngày t và nắm giữ suốt ngày t+1. Do đó lợi nhuận "
         "chiến lược là:")
    formula(doc, "r_strat(t) = position(t−1) × r(t)")
    para(doc,
         "Nếu viết thành position(t) × r(t) thì vị thế tại ngày t – được quyết "
         "định bằng thông tin của ngày t, trong đó có giá đóng cửa t – sẽ hưởng "
         "lợi nhuận của chính ngày t. Nhưng lợi nhuận ngày t đã được biết khi "
         "biết giá đóng cửa t, nghĩa là tín hiệu biết trước lợi nhuận mà nó sắp "
         "hưởng. Đây là lỗi phổ biến nhất trong backtest, thường cho kết quả rất "
         "ấn tượng nhưng hoàn toàn không có giá trị.")

    heading(doc, "2.6.2. Chi phí giao dịch", level=3)
    formula(doc, "turnover(t) = | position(t) − position(t−1) |")
    formula(doc, "cost(t) = turnover(t) × COST_BPS / 10.000")
    para(doc,
         "Chi phí chỉ phát sinh khi vị thế thay đổi và tỷ lệ với mức độ thay "
         "đổi. Chuyển từ Flat sang Long cho turnover bằng 1, còn chuyển từ Short "
         "sang Long cho turnover bằng 2 vì phải thực hiện hai giao dịch. Đề tài "
         "sử dụng mức 2 điểm cơ bản tương ứng 0,02% mỗi lần đổi vị thế, phản ánh "
         "spread điển hình của hợp đồng vàng tương lai thanh khoản cao. Việc bỏ "
         "qua chi phí là lỗi làm sai lệch backtest nghiêm trọng, đặc biệt với các "
         "chiến lược có tần suất giao dịch cao.")

    heading(doc, "2.6.3. Danh mục các chiến lược so sánh", level=3)
    table(doc,
          caption_title="Tám chiến lược giao dịch được so sánh",
          headers=["Chiến lược", "Trường phái", "Quy tắc phát sinh tín hiệu"],
          rows=[
              ["BuyHold", "Thụ động", "Vị thế Long trong toàn bộ giai đoạn"],
              ["TA_MA_Crossover", "Trend-following", "Long khi MA10 > MA30"],
              ["TA_MACD", "Trend-following", "Long khi MACD > Signal"],
              ["TA_RSI", "Mean-reversion",
               "Vào Long khi RSI < 30; thoát khi RSI > 70 (máy trạng thái)"],
              ["TA_Combined", "Trend có xác nhận kép",
               "Long khi đồng thời MA10 > MA30 và MACD > Signal"],
              ["AI_XGB_LongFlat", "Trí tuệ nhân tạo",
               "Long khi P(tăng) > 0,50; ngược lại Flat"],
              ["AI_XGB_LongShort", "Trí tuệ nhân tạo",
               "Long khi P(tăng) > 0,50; ngược lại Short"],
              ["AI_XGB_Conf60", "AI có bộ lọc tin cậy",
               "Long khi P(tăng) > 0,60; ngược lại Flat"],
          ],
          widths=[2.2, 1.9, 4.1],
          font_size=10,
          note="Nguồn: thiết kế của nhóm nghiên cứu.")

    para(doc,
         "Chiến lược TA_RSI được triển khai dưới dạng máy trạng thái thay vì "
         "điều kiện tức thời. Lý do là nếu chỉ dùng điều kiện “Long khi RSI nhỏ "
         "hơn 30” thì vị thế sẽ bị đóng ngay khi RSI vượt 30, trong khi logic "
         "hồi quy về trung bình là giữ vị thế cho đến khi giá phục hồi đến vùng "
         "quá mua. Máy trạng thái phản ánh đúng logic giao dịch thực tế.")
    para(doc,
         "Chiến lược BuyHold giữ vai trò benchmark bắt buộc. Một chiến lược chủ "
         "động chỉ tạo ra giá trị kinh tế nếu vượt được chiến lược nắm giữ thụ "
         "động sau chi phí giao dịch; nếu không, nhà đầu tư hợp lý sẽ chọn nắm "
         "giữ thụ động với chi phí gần bằng không.")

    heading(doc, "2.6.4. Cơ sở kinh tế của bộ lọc độ tin cậy", level=3)
    para(doc,
         "Chiến lược AI_XGB_Conf60 sử dụng ngưỡng 0,60 thay vì 0,50. Cơ sở là "
         "điều kiện để một giao dịch có kỳ vọng dương khi tính cả chi phí c. Giả "
         "định lợi nhuận và lỗ đối xứng với độ lớn kỳ vọng E|r|, điều kiện là:")
    formula(doc, "P(tăng) · E|r| − [1 − P(tăng)] · E|r| > c")
    formula(doc, "⇔  P(tăng) > 0,5 + c / ( 2 · E|r| )")
    para(doc,
         "Kết quả này có ý nghĩa quan trọng: ngưỡng tối ưu luôn lớn hơn 0,5 khi "
         "tồn tại chi phí giao dịch, và càng phải cao khi chi phí càng lớn hoặc "
         "biên độ biến động càng nhỏ. Đây là cơ sở lý luận định lượng cho việc "
         "không giao dịch khi lợi thế kỳ vọng không đủ bù chi phí.")

    # ---------------------------------------------------------------- 2.7
    heading(doc, "2.7. Hệ số quy đổi năm", level=2)
    para(doc,
         "Đây là một điểm kỹ thuật cần xử lý chính xác. Hệ số quy đổi năm P là "
         "số quan sát thực tế trong một năm của chuỗi dữ liệu, được dùng trong "
         "công thức quy đổi độ biến động và tỷ số Sharpe qua nhân tử √P. Vì bộ "
         "dữ liệu nghiên cứu chứa cả Thứ Bảy và Chủ Nhật nên có khoảng 365 quan "
         "sát mỗi năm, khác với 252 phiên của dữ liệu giao dịch thật. Nếu dùng "
         "sai P = 252, các chỉ số sẽ bị lệch theo tỷ lệ:")
    formula(doc, "√( 365 / 252 ) = 1,2035",
            note="Tức phóng đại khoảng 20,35%.")
    para(doc,
         "Mức sai lệch này đủ lớn để thay đổi kết luận so sánh: một chiến lược "
         "có Sharpe thật 2,107 sẽ bị báo thành 2,536. Do đó toàn bộ tính toán "
         "trong đề tài sử dụng P = 365 để khớp với tần số quan sát thật của "
         "chuỗi dữ liệu.")

    # ---------------------------------------------------------------- 2.8
    heading(doc, "2.8. Phương pháp phân tích đóng góp đặc trưng", level=2)
    para(doc,
         "Độ quan trọng đặc trưng nội bộ của XGBoost chỉ cho biết mô hình đã sử "
         "dụng biến nào nhiều, không cho biết biến đó có cải thiện năng lực dự "
         "báo ngoài mẫu hay không – một biến hoàn toàn là nhiễu vẫn có thể có "
         "Gain dương do mô hình quá khớp vào nó. Vì vậy đề tài sử dụng ablation "
         "study làm thiết kế chính: huấn luyện lại mô hình từ đầu với từng tập "
         "con đặc trưng cộng dồn và so sánh hiệu năng ngoài mẫu.")
    formula(doc, "M1 ⊂ M2 ⊂ M3 ⊂ M4")
    para(doc,
         "Điểm then chốt là mỗi mô hình được huấn luyện lại với cùng thiết kế "
         "walk-forward, nên chênh lệch AUC giữa các bậc là ước lượng không chệch "
         "của giá trị gia tăng của từng nhóm đặc trưng. Kết quả được đối chiếu "
         "với hai công cụ bổ trợ: độ quan trọng dạng Gain và giá trị SHAP "
         "(Lundberg và Lee, 2017). SHAP phân rã mỗi dự báo thành tổng đóng góp "
         "của từng biến dựa trên giá trị Shapley trong lý thuyết trò chơi hợp "
         "tác, có ưu điểm là tính cộng, tính nhất quán, và cho biết chiều tác "
         "động trên từng quan sát chứ không chỉ độ lớn tổng hợp.")
