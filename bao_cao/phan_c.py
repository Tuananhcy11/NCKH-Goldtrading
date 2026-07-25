# -*- coding: utf-8 -*-
"""PHAN C: Chuong 3 (ket qua), Chuong 4 (thao luan), Ket luan, TLTK, Phu luc."""
from docx.shared import Pt
from engine import para, heading, bullet, table, figure, formula

G = "../ket_qua/goc/"
D = "../ket_qua/doi_chung/"


def chuong_3(doc):
    heading(doc, "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU", level=1, align="center",
            page_break=True)

    para(doc,
         "Toàn bộ kết quả trình bày trong chương này được tính trên giai đoạn "
         "ngoài mẫu từ 19/02/2020 đến 29/12/2025 gồm 2.141 quan sát, với hệ số "
         "quy đổi năm P = 365 và chi phí giao dịch 2 điểm cơ bản mỗi lần đổi vị "
         "thế. Mô hình chưa từng tiếp cận dữ liệu của giai đoạn này trong quá "
         "trình huấn luyện tại từng vòng walk-forward.")

    # ---------------------------------------------------------------- 3.1
    heading(doc, "3.1. Chất lượng dự báo của mô hình", level=2)

    table(doc,
          caption_title="Chỉ tiêu chất lượng dự báo của mô hình XGBoost "
                        "trên tập ngoài mẫu",
          headers=["Chỉ tiêu", "Giá trị", "Mốc so sánh"],
          rows=[
              ["Accuracy", "**0,8389**", "Baseline (lớp đa số) = 0,7394"],
              ["F1-score", "0,8862", "—"],
              ["AUC", "**0,9299**", "Ngẫu nhiên = 0,5"],
              ["Precision", "0,9275", "—"],
              ["Recall", "0,8484", "—"],
              ["Specificity", "0,8118", "—"],
              ["Log Loss", "0,2906", "Đoán bừa = 0,6931"],
              ["Brier Score", "0,0962", "Đoán bừa = 0,2500"],
          ],
          widths=[2.2, 1.6, 3.2],
          note="Nguồn: kết quả chạy chương trình ai_vs_ta_original_data.py và "
               "phan_tich_xac_suat.py.")

    para(doc, "Ma trận nhầm lẫn của mô hình như sau:")
    table(doc,
          caption_title="Ma trận nhầm lẫn của mô hình XGBoost (N = 2.141)",
          headers=["", "Dự báo GIẢM", "Dự báo TĂNG", "Tổng"],
          rows=[
              ["**Thực tế GIẢM**", "453 (TN)", "105 (FP)", "558"],
              ["**Thực tế TĂNG**", "240 (FN)", "1.343 (TP)", "1.583"],
              ["**Tổng**", "693", "1.448", "2.141"],
          ],
          widths=[2.4, 1.9, 1.9, 1.2],
          note="Dự báo đúng: 1.796 quan sát (83,89%). Dự báo sai: 345 quan sát "
               "(16,11%).")

    para(doc,
         "Các tỷ lệ dẫn xuất từ ma trận nhầm lẫn có ý nghĩa giao dịch cụ thể. "
         "Precision đạt 0,9275 nghĩa là trong 1.448 lần mô hình báo giá tăng có "
         "1.343 lần đúng – đây là chỉ số quan trọng nhất với chiến lược chỉ mua "
         "vì nó phản ánh tỷ lệ lệnh mua có lãi. Recall đạt 0,8484 cho thấy mô "
         "hình bỏ lỡ 240 trong 1.583 ngày tăng. Specificity đạt 0,8118 phản ánh "
         "khả năng tránh lỗ, vì mỗi trường hợp dương tính giả là một lệnh mua bị "
         "lỗ.")
    para(doc,
         "Tuy nhiên, cần đặc biệt lưu ý khi diễn giải con số Accuracy 83,89%. Vì "
         "tỷ lệ lớp đa số trong tập ngoài mẫu là 73,94%, một mô hình vô dụng "
         "luôn dự báo tăng đã đạt Accuracy 73,94%. Do đó giá trị thực sự mô hình "
         "tạo thêm chỉ là 9,95 điểm phần trăm. Việc luôn báo cáo baseline kèm "
         "Accuracy là bắt buộc để tránh diễn giải quá lạc quan.")

    figure(doc, G + "hinh6_confusion_matrix_original.png",
           "Ma trận nhầm lẫn của mô hình XGBoost trên tập ngoài mẫu",
           width_cm=11.0,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    # ---------------------------------------------------------------- 3.2
    heading(doc, "3.2. Kết quả ablation study", level=2)
    para(doc,
         "Bốn mô hình được huấn luyện lại độc lập với các tập đặc trưng cộng dồn, "
         "sử dụng cùng thiết kế walk-forward, nhằm định lượng giá trị gia tăng "
         "của từng nhóm đặc trưng.")

    table(doc,
          caption_title="Kết quả ablation study – đóng góp của từng nhóm đặc trưng",
          headers=["Mô hình", "Số đặc trưng", "Accuracy", "F1", "AUC",
                   "AUC gia tăng"],
          rows=[
              ["M1 – Xu hướng", "4", "0,6240", "0,6943", "0,7989", "—"],
              ["M2 – thêm Động lượng", "7", "0,8108", "0,8649", "0,9117",
               "**+0,1128**"],
              ["M3 – thêm Biến động", "11", "0,8062", "0,8597", "0,9112",
               "−0,0005"],
              ["M4 – thêm Đặc trưng trễ", "14", "**0,8389**", "**0,8862**",
               "**0,9299**", "+0,0187"],
          ],
          widths=[2.6, 1.3, 1.3, 1.1, 1.1, 1.6],
          font_size=10,
          note="Nguồn: kết quả chạy chương trình ai_vs_ta_original_data.py.")

    para(doc,
         "Nhóm động lượng đóng góp lớn nhất với mức tăng 0,1128 điểm AUC, từ "
         "0,7989 lên 0,9117. Đóng góp này chủ yếu đến từ biến RSI14, phù hợp với "
         "lập luận ở mục 2.3.3: RSI là biến có thang đo cố định trong khoảng 0 "
         "đến 100, bất biến theo cả mức giá và thời gian, nên ngưỡng chia mà cây "
         "học được vẫn giữ nguyên hiệu lực ở giai đoạn ngoài mẫu.")
    para(doc,
         "Nhóm biến động cho kết quả thoạt nhìn nghịch lý: AUC gần như không "
         "thay đổi, giảm nhẹ 0,0005 điểm. Tuy nhiên nhóm này lại chiếm 14,85% "
         "tổng độ quan trọng Gain như trình bày ở mục 3.3. Đây không phải nghịch "
         "lý mà chính là bằng chứng thực nghiệm cho lập luận về chế độ thị trường "
         "ở mục 2.3.4: vai trò của nhóm biến động là điều kiện hóa các tín hiệu "
         "khác theo trạng thái thị trường chứ không phải dự báo độc lập. Mô hình "
         "sử dụng nhóm này nhiều để tinh chỉnh quy tắc phân chia, nhưng vì thông "
         "tin đó đã phần nào hàm chứa trong các biến khác nên năng lực xếp hạng "
         "tổng thể không tăng thêm.")
    para(doc,
         "Nhóm đặc trưng trễ đóng góp thêm 0,0187 điểm AUC. Theo giả thuyết hiệu "
         "quả dạng yếu, nhóm này lẽ ra không có năng lực dự báo. Kết quả kiểm "
         "định chất lượng dữ liệu ở mục 2.2 cùng phân tích hiệu chuẩn ở mục 3.4 "
         "cho thấy phần đóng góp này phần lớn xuất phát từ hiện tượng nội suy dữ "
         "liệu chứ không phải từ tính không hiệu quả thật của thị trường.")

    # ---------------------------------------------------------------- 3.3
    heading(doc, "3.3. Độ quan trọng đặc trưng", level=2)

    table(doc,
          caption_title="Độ quan trọng đặc trưng theo nhóm (Gain, %)",
          headers=["Nhóm đặc trưng", "Tỷ lệ đóng góp Gain (%)"],
          rows=[
              ["Nhóm 2 – Động lượng", "**54,66**"],
              ["Nhóm 4 – Đặc trưng trễ", "22,63"],
              ["Nhóm 3 – Biến động", "14,85"],
              ["Nhóm 1 – Xu hướng", "7,86"],
          ],
          widths=[3.4, 2.4],
          note="Nguồn: kết quả chạy chương trình ai_vs_ta_original_data.py.")

    table(doc,
          caption_title="Độ quan trọng của năm đặc trưng hàng đầu (Gain, %)",
          headers=["Đặc trưng", "Nhóm", "Gain (%)"],
          rows=[
              ["RSI14", "Động lượng", "**51,05**"],
              ["log_return_lag1", "Đặc trưng trễ", "19,06"],
              ["volatility_20d", "Biến động", "7,16"],
              ["BB_pctB", "Biến động", "3,54"],
              ["volume_ratio", "Biến động", "2,26"],
          ],
          widths=[2.6, 2.2, 1.6],
          note="Chín đặc trưng còn lại có mức đóng góp từ 1,57% đến 2,10%. "
               "Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    para(doc,
         "Hai biến RSI14 và log_return_lag1 chiếm tới 70,11% tổng độ quan trọng "
         "Gain. Mức tập trung này rất cao và cần được lưu ý: về cơ bản mô hình "
         "chỉ dựa vào hai tín hiệu, khiến nó dễ bị ảnh hưởng nếu quan hệ của hai "
         "biến đó thay đổi. Việc biến log_return_lag1 đứng thứ hai cũng đúng là "
         "trường hợp cần kiểm tra theo cảnh báo phương pháp luận đã nêu ở mục "
         "2.3.5.")

    figure(doc, G + "hinh4_ablation_original.png",
           "Kết quả ablation study và độ quan trọng Gain theo nhóm đặc trưng",
           width_cm=15.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    figure(doc, G + "hinh5_shap_original.png",
           "Biểu đồ SHAP thể hiện chiều và độ lớn tác động của từng đặc trưng",
           width_cm=14.0,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    # ---------------------------------------------------------------- 3.4
    heading(doc, "3.4. Phân tích đầu ra xác suất và mức độ hiệu chuẩn", level=2)

    heading(doc, "3.4.1. Phân biệt ba đại lượng", level=3)
    para(doc,
         "Mô hình XGBoost xuất ra xác suất giá tăng, chứ không phải xác suất dự "
         "báo đúng. Đây là điểm rất dễ nhầm lẫn cần được nêu chính xác. Ví dụ, "
         "P(tăng) = 0,20 là một dự báo rất tự tin rằng giá sẽ giảm, nên xác suất "
         "dự báo đúng của quan sát đó là 0,80 chứ không phải 0,20. Ba đại lượng "
         "cần phân biệt như sau.")

    table(doc,
          caption_title="Phân biệt ba đại lượng liên quan đến đầu ra xác suất",
          headers=["Đại lượng", "Công thức", "Giá trị\ntrung bình", "Bản chất"],
          rows=[
              ["P(tăng)", "sigmoid(F(x))", "0,6790",
               "Xác suất GIÁ TĂNG – đầu ra trực tiếp của mô hình"],
              ["Confidence", "max(P, 1−P)", "0,8464",
               "Xác suất DỰ BÁO ĐÚNG – mô hình tự đánh giá"],
              ["Accuracy", "(TP+TN)/N", "0,8389",
               "TỶ LỆ dự báo đúng – đếm thực tế trên dữ liệu"],
          ],
          widths=[1.6, 1.6, 1.3, 3.5],
          font_size=10,
          note="Chênh lệch giữa Confidence và Accuracy là +0,0075. "
               "Nguồn: kết quả chạy chương trình phan_tich_xac_suat.py.")

    para(doc,
         "Chênh lệch trung bình giữa mức tự tin và độ chính xác thực tế chỉ "
         "+0,0075, tức mô hình hơi quá tự tin nhưng ở mức không đáng kể. Tuy "
         "nhiên, chênh lệch trung bình nhỏ không bảo đảm mô hình được hiệu chuẩn "
         "tốt ở mọi mức xác suất. Phân tích theo từng khoảng dưới đây cho thấy "
         "một vấn đề nghiêm trọng bị che lấp bởi con số trung bình này.")

    heading(doc, "3.4.2. Độ chính xác theo mức độ tự tin", level=3)
    table(doc,
          caption_title="Độ chính xác thực tế của mô hình theo từng mức độ tự tin",
          headers=["Khoảng Confidence", "Số quan sát", "Confidence\ntrung bình",
                   "Accuracy\nthực tế", "Sai lệch"],
          rows=[
              ["0,50 – 0,55", "137", "0,5268", "0,5182", "+0,0086"],
              ["0,55 – 0,60", "174", "0,5759", "0,5172", "+0,0587"],
              ["0,60 – 0,70", "235", "0,6470", "0,5617", "+0,0853"],
              ["0,70 – 0,80", "168", "0,7475", "0,5893", "**+0,1582**"],
              ["0,80 – 1,00", "**1.427**", "0,9545", "**0,9839**", "−0,0294"],
          ],
          widths=[2.2, 1.4, 1.6, 1.5, 1.3],
          font_size=10,
          note="Nguồn: kết quả chạy chương trình phan_tich_xac_suat.py.")

    para(doc,
         "Bảng trên cho thấy một phát hiện quan trọng: mô hình phân tách thành "
         "hai chế độ hoàn toàn khác nhau. Ở chế độ thứ nhất, với 714 quan sát "
         "chiếm 33% tổng số có mức tự tin dưới 0,80, độ chính xác thực tế chỉ "
         "đạt từ 51,72% đến 58,93% – gần như ngang với tung đồng xu. Đặc biệt "
         "trong khoảng tự tin 0,70 – 0,80, mô hình tự nhận đúng 74,75% nhưng "
         "thực tế chỉ đúng 58,93%, sai lệch tới 15,82 điểm phần trăm. Ở chế độ "
         "thứ hai, với 1.427 quan sát chiếm 67% tổng số có mức tự tin trên 0,80, "
         "độ chính xác thực tế đạt 98,39% – gần như hoàn hảo.")
    para(doc,
         "Độ chính xác tổng thể 83,89% chính là kết quả trung bình của hai chế độ "
         "này:")
    formula(doc, "0,67 × 0,9839 + 0,33 × 0,5540 ≈ 0,8389")
    para(doc,
         "Nói cách khác, con số 83,89% không có nghĩa mô hình dự báo đúng gần 84% "
         "các phiên nhờ đọc được tín hiệu thị trường. Thực chất mô hình dự báo "
         "gần như hoàn hảo ở 67% quan sát và gần như ngẫu nhiên ở 33% còn lại. "
         "Một mô hình học được tín hiệu thị trường thật sẽ cho độ chính xác tăng "
         "dần và đều theo mức tự tin; phân bố lưỡng cực cực đoan như trên là dấu "
         "hiệu điển hình của việc mô hình phát hiện được một cấu trúc xác định "
         "trong dữ liệu chứ không phải cấu trúc xác suất của thị trường.")
    para(doc,
         "Điều đáng chú ý là tỷ lệ 33% quan sát ở chế độ ngẫu nhiên xấp xỉ đúng "
         "tỷ lệ ngày giao dịch thật trong bộ dữ liệu. Đây là bằng chứng độc lập "
         "thứ hai, bên cạnh kết quả kiểm định ở mục 2.2, cho thấy phần dự báo "
         "chính xác cao xuất phát từ các đoạn nội suy.")
    para(doc,
         "Ở góc độ ứng dụng, bảng trên cũng cho thấy một hàm ý tích cực: vì vùng "
         "tự tin cao thực sự có độ chính xác cao hơn, việc sử dụng ngưỡng tin cậy "
         "để lọc giao dịch là có căn cứ. Đây là cơ sở thực nghiệm cho chiến lược "
         "AI_XGB_Conf60.")

    figure(doc, G + "hinh7_hieu_chuan_xac_suat.png",
           "Đường hiệu chuẩn và phân bố xác suất dự báo của mô hình",
           width_cm=15.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    para(doc,
         "Biểu đồ bên phải minh họa rõ tính lưỡng cực của phân bố xác suất: các "
         "quan sát tập trung thành hai cụm ở hai đầu thang xác suất thay vì phân "
         "bố đều quanh giá trị 0,5 như thường thấy ở một mô hình dự báo thị "
         "trường tài chính.")

    # ---------------------------------------------------------------- 3.5
    heading(doc, "3.5. Kết quả so sánh hiệu quả các chiến lược", level=2)

    table(doc,
          caption_title="So sánh hiệu quả tám chiến lược giao dịch "
                        "trên giai đoạn ngoài mẫu",
          headers=["Chiến lược", "Tổng LN", "CAGR", "Biến\nđộng",
                   "Sharpe", "Sortino", "MaxDD", "Calmar"],
          rows=[
              ["AI_XGB_Conf60", "127,91%", "15,08%", "**3,09%**",
               "**4,568**", "1,929", "**−4,79%**", "**3,151**"],
              ["AI_XGB_LongFlat", "144,35%", "16,45%", "4,69%",
               "3,270", "1,726", "−7,44%", "2,212"],
              ["TA_MA_Crossover", "**189,15%**", "**19,84%**", "6,99%",
               "2,624", "1,434", "−7,21%", "2,754"],
              ["BuyHold", "174,64%", "18,80%", "8,34%",
               "2,107", "1,784", "−17,82%", "1,055"],
              ["AI_XGB_LongShort", "117,40%", "14,16%", "8,38%",
               "1,621", "1,321", "−14,12%", "1,003"],
              ["TA_Combined", "65,54%", "8,97%", "5,80%",
               "1,511", "0,654", "−9,16%", "0,980"],
              ["TA_MACD", "69,63%", "9,43%", "6,50%",
               "1,418", "0,715", "−15,49%", "0,608"],
              ["TA_RSI", "−2,02%", "−0,35%", "4,87%",
               "−0,047", "−0,035", "−20,27%", "−0,017"],
          ],
          widths=[2.3, 1.2, 1.0, 1.0, 1.0, 1.0, 1.1, 1.0],
          font_size=9,
          note="Sắp xếp theo tỷ số Sharpe giảm dần. Nguồn: kết quả chạy chương "
               "trình ai_vs_ta_original_data.py.")

    table(doc,
          caption_title="Đặc tính vận hành của các chiến lược",
          headers=["Chiến lược", "Win Rate", "Số lệnh", "Turnover\nmỗi năm",
                   "Tỷ lệ thời gian\ncó vị thế"],
          rows=[
              ["AI_XGB_Conf60", "91,53%", "130", "22,163", "61,0%"],
              ["AI_XGB_LongFlat", "86,13%", "218", "37,165", "67,6%"],
              ["TA_MA_Crossover", "86,82%", "29", "4,944", "76,8%"],
              ["BuyHold", "74,08%", "1", "0,170", "100,0%"],
              ["AI_XGB_LongShort", "83,25%", "218", "74,159", "100,0%"],
              ["TA_Combined", "80,60%", "58", "9,888", "37,5%"],
              ["TA_MACD", "77,66%", "64", "10,911", "42,5%"],
              ["TA_RSI", "27,88%", "22", "3,751", "23,8%"],
          ],
          widths=[2.3, 1.4, 1.2, 1.5, 1.8],
          font_size=10,
          note="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    figure(doc, G + "hinh1_equity_drawdown_original.png",
           "Đường giá trị tài sản và mức sụt giảm của các chiến lược "
           "trên giai đoạn ngoài mẫu",
           width_cm=15.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    figure(doc, G + "hinh2_risk_return_original.png",
           "Đánh đổi giữa hiệu quả điều chỉnh rủi ro và mức sụt giảm tối đa",
           width_cm=13.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    para(doc,
         "Kết quả cho thấy một bức tranh phân hóa rõ rệt theo từng tiêu chí. Về "
         "lợi nhuận tuyệt đối, chiến lược tín hiệu kỹ thuật TA_MA_Crossover dẫn "
         "đầu với 189,15%, thậm chí vượt cả benchmark thụ động BuyHold ở mức "
         "174,64%. Các chiến lược trí tuệ nhân tạo chỉ đạt từ 117,40% đến "
         "144,35%, thấp hơn đáng kể.")
    para(doc,
         "Ngược lại, về hiệu quả điều chỉnh rủi ro, các chiến lược trí tuệ nhân "
         "tạo vượt trội. Chiến lược AI_XGB_Conf60 đạt tỷ số Sharpe 4,568 so với "
         "2,624 của chiến lược kỹ thuật tốt nhất và 2,107 của BuyHold; đồng thời "
         "có độ biến động thấp nhất 3,09% so với 8,34% của BuyHold và mức sụt "
         "giảm tối đa nhỏ nhất −4,79% so với −17,82% của BuyHold, tức nhỏ hơn "
         "gần 3,7 lần.")
    para(doc,
         "Một điểm cần lưu ý khi diễn giải là chênh lệch giữa Sharpe và Sortino "
         "của chiến lược AI_XGB_Conf60: Sharpe đạt 4,568 nhưng Sortino chỉ 1,929. "
         "Theo lập luận ở mục 1.4.3, chênh lệch lớn này cho thấy tỷ số Sharpe cao "
         "chủ yếu nhờ độ lệch chuẩn tổng thể rất nhỏ chứ không nhờ phân bố lợi "
         "nhuận đặc biệt thuận lợi. Nếu chỉ nhìn Sharpe sẽ đánh giá quá lạc quan "
         "về chiến lược này.")
    para(doc,
         "Biến thể AI_XGB_LongShort cho kết quả kém hơn rõ rệt so với "
         "AI_XGB_LongFlat trên mọi chỉ tiêu rủi ro: Sharpe 1,621 so với 3,270 và "
         "mức sụt giảm −14,12% so với −7,44%. Theo lập luận thiết kế ở mục 2.6.3, "
         "đây là bằng chứng cho thấy mô hình dự báo tốt chủ yếu ở một chiều – "
         "chiều tăng, trùng với xu hướng chung của giai đoạn 2020 – 2025 – chứ "
         "không thực sự dự báo được cả hai chiều. Ngoài ra chiến lược này có "
         "turnover 74,159 lần mỗi năm, cao nhất trong tất cả, nên chịu ma sát chi "
         "phí lớn nhất.")
    para(doc,
         "Chiến lược TA_RSI cho tổng lợi nhuận âm −2,02% với Win Rate chỉ 27,88%. "
         "Điều này phản ánh đặc điểm của giai đoạn kiểm định: trong một thị "
         "trường tăng giá mạnh và bền, chiến lược hồi quy về trung bình liên tục "
         "bán ra khi giá vào vùng quá mua, do đó bỏ lỡ phần lớn xu hướng tăng.")

    # ---------------------------------------------------------------- 3.6
    heading(doc, "3.6. Kết quả kiểm định tính ổn định", level=2)

    table(doc,
          caption_title="Lợi nhuận theo từng năm của các chiến lược (%)",
          headers=["Năm", "BuyHold", "TA_MA", "TA_MACD", "TA_RSI",
                   "TA_Comb", "AI_LF", "AI_LS", "AI_C60"],
          rows=[
              ["2020", "17,74", "20,70", "−1,92", "0,48", "−2,08",
               "15,41", "13,12", "15,48"],
              ["2021", "−3,47", "2,88", "−1,93", "−4,77", "4,77",
               "1,86", "7,47", "9,43"],
              ["2022", "−0,15", "8,35", "−1,44", "−7,06", "−5,50",
               "6,80", "14,24", "1,95"],
              ["2023", "13,08", "6,74", "11,67", "3,01", "9,11",
               "7,32", "1,85", "7,52"],
              ["2024", "27,42", "22,31", "5,92", "5,78", "4,25",
               "23,17", "19,06", "20,75"],
              ["2025", "67,95", "64,62", "51,27", "1,11", "50,11",
               "47,23", "29,07", "36,25"],
          ],
          widths=[0.8, 1.3, 1.1, 1.3, 1.1, 1.2, 1.0, 1.0, 1.1],
          font_size=9,
          note="AI_LF = AI_XGB_LongFlat; AI_LS = AI_XGB_LongShort; "
               "AI_C60 = AI_XGB_Conf60; TA_Comb = TA_Combined. "
               "Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    table(doc,
          caption_title="Các chỉ tiêu tính ổn định của chiến lược",
          headers=["Chiến lược", "Độ lệch chuẩn\nlợi nhuận năm",
                   "Tỷ lệ năm\ncó lãi", "Năm xấu nhất"],
          rows=[
              ["TA_RSI", "**4,82**", "66,67%", "−7,06%"],
              ["AI_XGB_LongShort", "9,42", "**100,00%**", "**+1,85%**"],
              ["AI_XGB_Conf60", "12,18", "**100,00%**", "**+1,95%**"],
              ["AI_XGB_LongFlat", "16,62", "**100,00%**", "**+1,86%**"],
              ["TA_Combined", "20,28", "66,67%", "−5,50%"],
              ["TA_MACD", "20,67", "50,00%", "−1,93%"],
              ["TA_MA_Crossover", "22,79", "**100,00%**", "**+2,88%**"],
              ["BuyHold", "25,93", "66,67%", "−3,47%"],
          ],
          widths=[2.4, 2.0, 1.6, 1.6],
          font_size=10,
          note="Sắp xếp theo độ lệch chuẩn lợi nhuận năm tăng dần. "
               "Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    figure(doc, G + "hinh3_loi_nhuan_nam_original.png",
           "Lợi nhuận theo từng năm của các chiến lược",
           width_cm=15.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    para(doc,
         "Kết quả cho thấy cả ba biến thể chiến lược trí tuệ nhân tạo đều có "
         "100% số năm có lãi, và năm xấu nhất vẫn cho lợi nhuận dương từ +1,85% "
         "đến +1,95%. Trong nhóm chiến lược kỹ thuật, chỉ TA_MA_Crossover đạt "
         "được đặc tính này; TA_MACD chỉ có lãi ở 50% số năm, còn TA_RSI và "
         "TA_Combined lãi ở 66,67% số năm. Benchmark BuyHold cũng chỉ lãi ở "
         "66,67% số năm và có độ lệch chuẩn lợi nhuận năm cao nhất là 25,93.")
    para(doc,
         "Cần đặc biệt lưu ý khi đọc bảng chỉ tiêu ổn định: chiến lược TA_RSI có "
         "độ lệch chuẩn lợi nhuận năm nhỏ nhất là 4,82 nhưng đây không phải "
         "chiến lược ổn định tốt nhất, vì tổng lợi nhuận của nó âm và chỉ 66,67% "
         "số năm có lãi. Đây là trường hợp ổn định trong việc không sinh lợi. "
         "Nhận xét này minh họa cho nguyên tắc đã nêu ở mục 1.4.4 rằng ba chỉ "
         "tiêu ổn định phải được đọc đồng thời.")

    # ---------------------------------------------------------------- 3.7
    heading(doc, "3.7. Thí nghiệm đối chứng trên dữ liệu độc lập", level=2)
    para(doc,
         "Để định lượng mức độ ảnh hưởng của vấn đề chất lượng dữ liệu phát hiện "
         "ở mục 2.2, đề tài thực hiện lại toàn bộ quy trình trên một nguồn dữ "
         "liệu vàng độc lập chỉ gồm các phiên giao dịch thật, với cùng tập đặc "
         "trưng và cùng thiết kế walk-forward.")

    table(doc,
          caption_title="So sánh kết quả giữa bộ dữ liệu đề tài "
                        "và dữ liệu đối chứng",
          headers=["Chỉ tiêu", "Bộ dữ liệu đề tài\n(có nội suy)",
                   "Dữ liệu đối chứng\n(phiên thật)"],
          rows=[
              ["Số quan sát", "4.016 (≈365/năm)", "2.764 (≈251/năm)"],
              ["Tỷ lệ bước giá trùng lặp", "76,07%", "0,18%"],
              ["Tự tương quan log-return bậc 1", "0,0415", "−0,0310"],
              ["Tỷ lệ ngày tăng giá", "66,13%", "53,06%"],
              ["Số quan sát Thứ Bảy và Chủ Nhật", "1.148", "0"],
              ["**AUC của mô hình**", "**0,9299**", "**0,5012**"],
              ["**Accuracy của mô hình**", "**0,8389**", "**0,5003**"],
              ["Baseline accuracy", "0,7394", "0,5540"],
              ["Sharpe chiến lược AI", "3,270", "0,576"],
          ],
          widths=[3.4, 2.3, 2.3],
          font_size=10,
          note="Nguồn: kết quả chạy chương trình ai_vs_ta_original_data.py và "
               "strategy_comparison.py.")

    para(doc,
         "Chỉ số AUC giảm từ 0,9299 xuống 0,5012 khi loại bỏ các quan sát nội "
         "suy. Vì AUC bằng 0,5 tương đương với dự báo ngẫu nhiên hoàn toàn, kết "
         "quả này cho thấy gần như toàn bộ năng lực dự báo quan sát được trên bộ "
         "dữ liệu đề tài xuất phát từ hiện tượng nội suy chứ không phải từ tín "
         "hiệu thị trường.")
    para(doc,
         "Kết quả AUC 0,5012 trên dữ liệu phiên thật nhất quán với dự đoán của "
         "Giả thuyết Thị trường Hiệu quả dạng yếu trình bày ở mục 1.1.1: tập chỉ "
         "báo kỹ thuật thuần – vốn đều là hàm của chuỗi giá quá khứ – không chứa "
         "thông tin dự báo hướng biến động giá vàng cho ngày kế tiếp. Ý nghĩa của "
         "phát hiện này được thảo luận ở mục 4.3 và 4.5.1.")

    figure(doc, D + "strategy_comparison_equity.png",
           "Đường giá trị tài sản của các chiến lược trên dữ liệu đối chứng",
           width_cm=15.5,
           source="Nguồn: kết quả tính toán của nhóm nghiên cứu.")


def chuong_4(doc):
    heading(doc, "CHƯƠNG 4. THẢO LUẬN", level=1, align="center",
            page_break=True)

    # ---------------------------------------------------------------- 4.1
    heading(doc, "4.1. Đánh giá theo ba tiêu chí của đề tài", level=2)

    heading(doc, "4.1.1. Tiêu chí lợi nhuận", level=3)
    para(doc,
         "Trên tiêu chí lợi nhuận tuyệt đối, chiến lược tín hiệu kỹ thuật thắng. "
         "TA_MA_Crossover đạt tổng lợi nhuận 189,15% và CAGR 19,84%, vượt cả "
         "benchmark thụ động. Các chiến lược trí tuệ nhân tạo đạt từ 117,40% đến "
         "144,35%, thấp hơn từ 45 đến 72 điểm phần trăm. Nguyên nhân chủ yếu là "
         "các chiến lược trí tuệ nhân tạo chỉ có vị thế trong 61% đến 68% thời "
         "gian, nên bỏ lỡ một phần xu hướng tăng của giai đoạn, cộng thêm ma sát "
         "chi phí do turnover cao.")

    heading(doc, "4.1.2. Tiêu chí mức độ rủi ro", level=3)
    para(doc,
         "Trên tiêu chí rủi ro, chiến lược trí tuệ nhân tạo thắng rõ rệt. Chiến "
         "lược AI_XGB_Conf60 có độ biến động 3,09%, chỉ bằng khoảng 37% mức "
         "8,34% của BuyHold, và mức sụt giảm tối đa −4,79% so với −17,82%. Về "
         "hiệu quả điều chỉnh rủi ro, chiến lược này đạt Sharpe 4,568 và Calmar "
         "3,151, cao nhất trong toàn bộ tám chiến lược. Kết quả này có ý nghĩa "
         "thực tiễn quan trọng: với nhà đầu tư có mức chấp nhận rủi ro thấp, "
         "việc giảm mức sụt giảm tối đa từ gần 18% xuống dưới 5% có giá trị lớn "
         "hơn phần lợi nhuận danh nghĩa bị hy sinh, vì mức sụt giảm quyết định "
         "khả năng trụ lại với chiến lược trong thực tế.")

    heading(doc, "4.1.3. Tiêu chí tính ổn định", level=3)
    para(doc,
         "Trên tiêu chí ổn định, chiến lược trí tuệ nhân tạo cũng thắng. Cả ba "
         "biến thể đều có 100% số năm có lãi với năm xấu nhất vẫn dương, trong "
         "khi trong nhóm kỹ thuật chỉ TA_MA_Crossover đạt được và benchmark "
         "BuyHold chỉ lãi ở 66,67% số năm. Đặc tính này phản ánh khả năng của mô "
         "hình trong việc đứng ngoài thị trường ở các giai đoạn bất lợi – cụ thể "
         "là năm 2021 và 2022 khi BuyHold lỗ lần lượt 3,47% và 0,15% thì cả ba "
         "biến thể trí tuệ nhân tạo đều có lãi.")

    heading(doc, "4.1.4. Kết luận tổng hợp về so sánh hai cách tiếp cận", level=3)
    para(doc,
         "Tổng hợp ba tiêu chí, kết quả nghiên cứu không cho phép khẳng định một "
         "cách tiếp cận vượt trội tuyệt đối. Chiến lược trí tuệ nhân tạo không "
         "thắng về lợi nhuận tuyệt đối nhưng vượt trội về hiệu quả điều chỉnh rủi "
         "ro và tính ổn định. Kết luận có tính điều kiện: lựa chọn giữa hai cách "
         "tiếp cận phụ thuộc vào hàm mục tiêu của nhà đầu tư. Nhà đầu tư tối đa "
         "hóa lợi nhuận tuyệt đối và chấp nhận sụt giảm sâu sẽ chọn chiến lược "
         "kỹ thuật theo xu hướng hoặc nắm giữ thụ động; nhà đầu tư ưu tiên ổn "
         "định và giới hạn sụt giảm sẽ chọn chiến lược trí tuệ nhân tạo.")

    # ---------------------------------------------------------------- 4.2
    heading(doc, "4.2. Thảo luận về vai trò của bộ lọc độ tin cậy", level=2)
    para(doc,
         "Một phát hiện đáng chú ý là biến thể AI_XGB_Conf60 cải thiện đồng thời "
         "cả ba tiêu chí so với biến thể cơ bản AI_XGB_LongFlat.")

    table(doc,
          caption_title="Tác động của bộ lọc độ tin cậy đến hiệu quả chiến lược",
          headers=["Chỉ tiêu", "AI_XGB_LongFlat\n(ngưỡng 0,50)",
                   "AI_XGB_Conf60\n(ngưỡng 0,60)", "Thay đổi"],
          rows=[
              ["Tỷ số Sharpe", "3,270", "4,568", "Tăng 39,7%"],
              ["Mức sụt giảm tối đa", "−7,44%", "−4,79%", "Giảm rủi ro 35,6%"],
              ["Calmar", "2,212", "3,151", "Tăng 42,4%"],
              ["Độ biến động", "4,69%", "3,09%", "Giảm 34,1%"],
              ["Turnover mỗi năm", "37,165", "22,163", "Giảm chi phí 40,4%"],
              ["Tổng lợi nhuận", "144,35%", "127,91%", "Giảm 16,44 điểm %"],
          ],
          widths=[2.4, 2.2, 2.2, 2.0],
          font_size=10,
          note="Nguồn: kết quả tính toán của nhóm nghiên cứu.")

    para(doc,
         "Kết quả này xác nhận bằng thực nghiệm lập luận lý thuyết ở mục 2.6.4 "
         "rằng ngưỡng phân loại tối ưu phải lớn hơn 0,5 khi tồn tại chi phí giao "
         "dịch. Cơ chế cải thiện gồm hai thành phần. Thứ nhất là giảm ma sát chi "
         "phí: turnover giảm 40,4% tương ứng chi phí giao dịch hàng năm giảm từ "
         "khoảng 0,74% xuống 0,44%. Thứ hai, và quan trọng hơn, là loại bỏ các "
         "giao dịch ở vùng mà mô hình thực chất không có năng lực dự báo – như "
         "phân tích ở mục 3.4.2, trong vùng tự tin dưới 0,80 độ chính xác thực "
         "tế chỉ khoảng 52% đến 59%. Việc không giao dịch ở vùng này giúp tránh "
         "các quyết định gần như ngẫu nhiên nhưng vẫn phải trả chi phí.")
    para(doc,
         "Hàm ý phương pháp luận rút ra là: khi triển khai mô hình học máy trong "
         "giao dịch, việc phân tích mức độ hiệu chuẩn của đầu ra xác suất có giá "
         "trị thực tiễn cao hơn việc chỉ tối ưu độ chính xác tổng thể. Một mô "
         "hình có độ chính xác trung bình nhưng hiệu chuẩn tốt cho phép thiết kế "
         "bộ lọc hiệu quả, trong khi một mô hình có độ chính xác cao nhưng hiệu "
         "chuẩn kém sẽ dẫn tới các quyết định sai ở những thời điểm mô hình tưởng "
         "rằng mình đúng.")

    # ---------------------------------------------------------------- 4.3
    heading(doc, "4.3. Thảo luận về đối chiếu lý thuyết", level=2)
    para(doc,
         "Kết quả trên bộ dữ liệu đề tài với AUC 0,9299 thoạt nhìn mâu thuẫn với "
         "Giả thuyết Thị trường Hiệu quả dạng yếu. Tuy nhiên thí nghiệm đối "
         "chứng ở mục 3.7 cho AUC 0,5012 trên dữ liệu phiên giao dịch thật – kết "
         "quả này lại nhất quán hoàn toàn với dự đoán của lý thuyết. Sự đối lập "
         "giữa hai kết quả có ý nghĩa phương pháp luận quan trọng.")
    para(doc,
         "Thứ nhất, nó cho thấy tầm quan trọng của bước kiểm định chất lượng dữ "
         "liệu. Nếu bỏ qua bước này, nghiên cứu sẽ đi tới kết luận rằng chỉ báo "
         "kỹ thuật có năng lực dự báo rất cao đối với giá vàng – một kết luận sai "
         "về bản chất, nhưng lại được hỗ trợ bởi các chỉ số thống kê trông rất "
         "thuyết phục.")
    para(doc,
         "Thứ hai, nó minh họa cho luận điểm rằng các chỉ số đánh giá tổng hợp có "
         "thể che lấp vấn đề. Trong nghiên cứu này, ba dấu hiệu độc lập cùng chỉ "
         "về một nguyên nhân: kết quả kiểm định cấu trúc dữ liệu ở mục 2.2, phân "
         "bố lưỡng cực của độ chính xác theo mức tự tin ở mục 3.4.2, và chênh "
         "lệch AUC giữa hai nguồn dữ liệu ở mục 3.7. Việc sử dụng nhiều góc độ "
         "chẩn đoán thay vì một chỉ số duy nhất là điều kiện để phát hiện vấn đề.")
    para(doc,
         "Thứ ba, kết quả AUC 0,5012 trên dữ liệu thật không có nghĩa toàn bộ "
         "nghiên cứu vô giá trị. Nó xác lập một kết luận có ý nghĩa khoa học: đối "
         "với bài toán dự báo hướng giá vàng cho một ngày kế tiếp, tập chỉ báo "
         "kỹ thuật nội sinh không đủ để tạo ra năng lực dự báo. Đây là kết quả "
         "âm tính nhưng hữu ích, vì nó chỉ ra hướng cải thiện là bổ sung thông "
         "tin ngoài chuỗi giá thay vì tinh chỉnh thêm các chỉ báo kỹ thuật.")

    # ---------------------------------------------------------------- 4.4
    heading(doc, "4.4. Thảo luận về đặc tính giai đoạn kiểm định", level=2)
    para(doc,
         "Giai đoạn ngoài mẫu 2020 – 2025 là thị trường tăng giá mạnh của vàng "
         "với BuyHold đạt 174,64% toàn kỳ và riêng năm 2025 tăng 67,95%. Đặc tính "
         "này tạo ra thiên lệch cấu trúc có lợi cho các chiến lược nắm giữ dài và "
         "bất lợi cho các chiến lược có lúc đứng ngoài thị trường.")
    para(doc,
         "Hệ quả cụ thể là kết luận về tiêu chí lợi nhuận có độ tin cậy thấp hơn "
         "kết luận về hai tiêu chí còn lại. Việc chiến lược trí tuệ nhân tạo thua "
         "về lợi nhuận tuyệt đối có thể phần lớn là hệ quả của đặc tính giai đoạn "
         "chứ không phải hạn chế nội tại của phương pháp. Ngược lại, ưu thế về "
         "mức sụt giảm tối đa và tỷ lệ năm có lãi phản ánh khả năng thực sự của "
         "mô hình trong việc nhận diện và tránh các giai đoạn bất lợi, nên có độ "
         "tin cậy cao hơn.")
    para(doc,
         "Kết quả năm 2022 minh họa rõ điểm này: BuyHold lỗ 0,15% và TA_RSI lỗ "
         "7,06%, trong khi AI_XGB_LongShort lãi 14,24% và AI_XGB_LongFlat lãi "
         "6,80%. Đây là năm duy nhất trong giai đoạn mà thị trường vàng đi ngang, "
         "và cũng là năm chiến lược trí tuệ nhân tạo thể hiện ưu thế rõ nhất so "
         "với các cách tiếp cận khác.")

    # ---------------------------------------------------------------- 4.5
    heading(doc, "4.5. Hạn chế của nghiên cứu", level=2)

    heading(doc, "4.5.1. Hạn chế về chất lượng dữ liệu", level=3)
    para(doc,
         "Đây là hạn chế quan trọng nhất cần nêu rõ. Bộ dữ liệu nghiên cứu chứa "
         "1.148 quan sát vào Thứ Bảy và Chủ Nhật, với 76,07% bước giá là kết quả "
         "nội suy tuyến tính. Vì giá ngày không giao dịch được suy ra từ giá ngày "
         "giao dịch kế sau, tồn tại rò rỉ thông tin tương lai ngay trong dữ liệu "
         "đầu vào. Hệ quả định lượng là các chỉ số Accuracy 0,8389 và AUC 0,9299 "
         "cao hơn đáng kể so với năng lực dự báo thực tế, như thí nghiệm đối "
         "chứng ở mục 3.7 đã chứng minh. Các kết luận về hiệu quả chiến lược "
         "trong Chương 3 vì vậy phải được diễn giải kèm hạn chế này.")

    heading(doc, "4.5.2. Hạn chế về phạm vi giai đoạn kiểm định", level=3)
    para(doc,
         "Giai đoạn ngoài mẫu chỉ bao phủ khoảng 5,9 năm và toàn bộ nằm trong "
         "một chu kỳ tăng giá. Để kiểm định tính bền vững của kết luận, cần bổ "
         "sung các giai đoạn có đặc tính khác, ví dụ giai đoạn 2013 – 2018 khi "
         "giá vàng đi ngang hoặc giảm.")

    heading(doc, "4.5.3. Hạn chế về mô hình hóa chi phí", level=3)
    para(doc,
         "Đề tài giả định chi phí cố định 2 điểm cơ bản mỗi lần đổi vị thế, chưa "
         "mô hình hóa trượt giá tăng theo quy mô lệnh, spread giãn rộng trong "
         "giai đoạn biến động cao, và chi phí qua đêm với vị thế đòn bẩy. Với "
         "chiến lược có turnover 37 lần mỗi năm, kết quả nhạy cảm với giả định "
         "này: nếu chi phí thực là 5 điểm cơ bản, chi phí hàng năm tăng từ 0,74% "
         "lên 1,86%, đủ để thay đổi thứ hạng so sánh.")

    heading(doc, "4.5.4. Hạn chế về tập đặc trưng", level=3)
    para(doc,
         "Toàn bộ 14 đặc trưng là hàm của chuỗi giá và khối lượng, tức đặc trưng "
         "nội sinh. Theo lập luận ở Chương 1, các chỉ báo kỹ thuật không bổ sung "
         "thông tin mới ngoài những gì đã có trong chuỗi giá, nên việc thêm chỉ "
         "báo cùng loại khó cải thiện năng lực dự báo. Việc chưa đưa vào các biến "
         "ngoại sinh có cơ sở kinh tế đối với giá vàng là hạn chế đáng kể, đồng "
         "thời là hướng mở rộng có cơ sở lý luận mạnh nhất.")

    heading(doc, "4.5.5. Hạn chế về kiểm định thống kê", level=3)
    para(doc,
         "Đề tài chưa kiểm định ý nghĩa thống kê của chênh lệch tỷ số Sharpe giữa "
         "các chiến lược. Chênh lệch giữa 4,568 và 2,624 có thể một phần do ngẫu "
         "nhiên, cần kiểm định Jobson – Korkie có hiệu chỉnh Memmel hoặc phương "
         "pháp bootstrap để xác nhận. Ngoài ra, việc thử nghiệm nhiều biến thể "
         "chiến lược rồi báo cáo kết quả tốt nhất tạo ra thiên lệch lựa chọn theo "
         "cảnh báo của Bailey và López de Prado (2014), nên chỉ tiêu Deflated "
         "Sharpe Ratio cần được bổ sung.")

    heading(doc, "4.5.6. Các hạn chế khác", level=3)
    bullet(doc, "Các chiến lược chỉ sử dụng vị thế toàn phần hoặc bằng không, "
                "chưa xét quản lý khối lượng vị thế theo biến động – một kỹ "
                "thuật thường cải thiện tỷ số Sharpe.")
    bullet(doc, "Siêu tham số được chọn theo cơ sở lý luận thay vì tìm kiếm hệ "
                "thống. Đây là lựa chọn có chủ đích để tránh quá khớp vào tập "
                "kiểm định, nhưng có nghĩa kết quả chưa phải tối ưu.")
    bullet(doc, "Mô hình tập trung quá mức vào hai biến RSI14 và log_return_lag1 "
                "chiếm 70,11% tổng Gain, làm giảm tính bền vững nếu quan hệ của "
                "hai biến này thay đổi.")
    bullet(doc, "Nghiên cứu chỉ xét một tài sản và một khung thời gian, nên tính "
                "khái quát của kết luận sang các tài sản khác chưa được kiểm "
                "chứng.")


def ket_luan_kien_nghi(doc):
    """3.11. Ket luan va kien nghi."""
    heading(doc, "KẾT LUẬN VÀ KIẾN NGHỊ", level=1, align="center",
            page_break=True)

    # ---------------------------------------------------------------- A
    heading(doc, "A. KẾT LUẬN", level=2)

    heading(doc, "1. Kết luận về các nội dung nghiên cứu đã thực hiện", level=3)
    para(doc,
         "Đề tài đã hoàn thành sáu nội dung nghiên cứu đề ra. Về mặt mô hình, "
         "nhóm đã xây dựng tập 14 đặc trưng thuộc bốn nhóm và huấn luyện mô hình "
         "XGBoost dự báo hướng biến động giá vàng theo thiết kế walk-forward trên "
         "giai đoạn ngoài mẫu gồm 2.141 quan sát. Về mặt chiến lược, nhóm đã xây "
         "dựng và backtest tám chiến lược giao dịch có tính chi phí, gồm một "
         "benchmark thụ động, bốn chiến lược tín hiệu kỹ thuật thuộc hai trường "
         "phái đối lập và ba biến thể chiến lược dựa trên trí tuệ nhân tạo.")

    heading(doc, "2. Kết luận về so sánh hai cách tiếp cận", level=3)
    para(doc,
         "Kết quả so sánh theo ba tiêu chí của đề tài cho thấy không có cách tiếp "
         "cận nào vượt trội tuyệt đối. Trên tiêu chí lợi nhuận tuyệt đối, chiến "
         "lược tín hiệu kỹ thuật theo xu hướng dẫn đầu với tổng lợi nhuận 189,15% "
         "so với 117,40% đến 144,35% của các chiến lược trí tuệ nhân tạo. Trên "
         "tiêu chí mức độ rủi ro và tính ổn định, chiến lược trí tuệ nhân tạo "
         "vượt trội rõ rệt: tỷ số Sharpe cao nhất đạt 4,568 so với 2,624, mức "
         "sụt giảm tối đa nhỏ nhất −4,79% so với −17,82% của benchmark thụ động, "
         "và cả ba biến thể đều có 100% số năm có lãi.")
    para(doc,
         "Kết luận vì vậy mang tính điều kiện: lựa chọn giữa hai cách tiếp cận "
         "phụ thuộc vào hàm mục tiêu và mức chấp nhận rủi ro của nhà đầu tư, chứ "
         "không thể quy về một thứ hạng duy nhất.")

    heading(doc, "3. Kết luận về đóng góp của các nhóm đặc trưng", level=3)
    para(doc,
         "Ablation study cho thấy nhóm chỉ báo động lượng đóng góp lớn nhất với "
         "mức tăng 0,1128 điểm AUC, chủ yếu từ biến RSI14 chiếm 51,05% tổng độ "
         "quan trọng Gain. Nhóm biến động không tăng AUC trực tiếp nhưng chiếm "
         "14,85% Gain, xác nhận vai trò điều kiện hóa các tín hiệu khác theo chế "
         "độ thị trường – đây cũng là cơ sở thực nghiệm cho việc lựa chọn mô hình "
         "cây thay vì mô hình tuyến tính.")

    heading(doc, "4. Kết luận về giới hạn năng lực dự báo thực tế", level=3)
    para(doc,
         "Thí nghiệm đối chứng trên dữ liệu chỉ gồm phiên giao dịch thật cho AUC "
         "0,5012 và Accuracy 0,5003 – tương đương dự báo ngẫu nhiên. Kết quả này "
         "nhất quán với Giả thuyết Thị trường Hiệu quả dạng yếu và cho phép kết "
         "luận rằng tập chỉ báo kỹ thuật nội sinh không đủ để tạo ra năng lực dự "
         "báo hướng giá vàng cho một ngày kế tiếp. Đây là kết luận âm tính nhưng "
         "có giá trị định hướng cho các nghiên cứu tiếp theo.")

    heading(doc, "5. Những đóng góp mới của đề tài", level=3)
    bullet(doc, "Thiết lập một quy trình so sánh có kiểm soát giữa chiến lược "
                "trí tuệ nhân tạo và chiến lược kỹ thuật trên cùng dữ liệu, cùng "
                "thiết kế kiểm định và cùng hệ chỉ tiêu, khắc phục hạn chế thiếu "
                "khả năng so sánh của các nghiên cứu trước.",
           bold_prefix="Về phương pháp: ")
    bullet(doc, "Chỉ ra rằng phân tích mức độ hiệu chuẩn của đầu ra xác suất có "
                "giá trị thực tiễn cao hơn việc tối ưu độ chính xác tổng thể, và "
                "chứng minh bằng thực nghiệm rằng bộ lọc độ tin cậy cải thiện "
                "đồng thời cả ba tiêu chí đánh giá.",
           bold_prefix="Về diễn giải mô hình: ")
    bullet(doc, "Đề xuất và áp dụng bộ ba phép kiểm định chất lượng dữ liệu trước "
                "khi diễn giải kết quả dự báo, cùng thiết kế thí nghiệm đối chứng "
                "trên nguồn dữ liệu độc lập – bước thường bị bỏ qua trong các "
                "nghiên cứu tương tự.",
           bold_prefix="Về kiểm soát chất lượng: ")
    bullet(doc, "Cung cấp bằng chứng định lượng cho thấy chỉ báo kỹ thuật nội "
                "sinh không đủ dự báo hướng giá vàng ngắn hạn, qua đó xác định "
                "hướng cải thiện là bổ sung thông tin ngoài chuỗi giá.",
           bold_prefix="Về kết quả thực nghiệm: ")

    heading(doc, "6. Khả năng ứng dụng của kết quả nghiên cứu", level=3)
    para(doc,
         "Kết quả nghiên cứu có ba khả năng ứng dụng. Thứ nhất, bảng so sánh "
         "đánh đổi lợi nhuận – rủi ro cung cấp căn cứ định lượng để nhà đầu tư "
         "lựa chọn chiến lược phù hợp với mức chấp nhận rủi ro của mình. Thứ hai, "
         "cơ chế bộ lọc độ tin cậy có thể áp dụng trực tiếp cho bất kỳ mô hình "
         "phân loại nào xuất ra xác suất, không giới hạn ở XGBoost hay thị trường "
         "vàng. Thứ ba, bộ chương trình gồm năm module độc lập theo chức năng có "
         "tính tái sử dụng cao, có thể áp dụng cho các tài sản khác mà không cần "
         "thay đổi cấu trúc.")

    # ---------------------------------------------------------------- B
    heading(doc, "B. KIẾN NGHỊ", level=2)

    heading(doc, "1. Kiến nghị về hoàn thiện dữ liệu nghiên cứu", level=3)
    para(doc,
         "Kiến nghị đầu tiên và quan trọng nhất là sử dụng dữ liệu chỉ gồm các "
         "phiên giao dịch thật, loại bỏ hoàn toàn các quan sát được điền bằng nội "
         "suy. Quy trình kiểm định gồm ba phép kiểm định trình bày ở mục 2.2 nên "
         "được thực hiện bắt buộc với mọi bộ dữ liệu trước khi mô hình hóa. Khi "
         "sử dụng dữ liệu tần số ngày, cần kiểm tra phân bố quan sát theo ngày "
         "trong tuần như một bước xác minh tối thiểu.")

    heading(doc, "2. Kiến nghị về các nghiên cứu tiếp theo", level=3)
    bullet(doc, "Bổ sung các biến ngoại sinh có cơ sở kinh tế đối với giá vàng: "
                "chỉ số đồng đô la Mỹ, lợi suất thực trái phiếu Mỹ, chỉ số biến "
                "động VIX, kỳ vọng lạm phát và các biến chính sách tiền tệ. Đây "
                "là hướng có cơ sở lý luận mạnh nhất, vì các chỉ báo kỹ thuật "
                "không bổ sung thông tin ngoài chuỗi giá.",
           bold_prefix="Hướng 1 – Mở rộng tập đặc trưng: ")
    bullet(doc, "Thử nghiệm dự báo cho horizon 5 ngày hoặc 10 ngày thay vì 1 "
                "ngày. Tín hiệu ở horizon dài thường có tỷ lệ tín hiệu trên "
                "nhiễu cao hơn, đồng thời giảm turnover và chi phí giao dịch.",
           bold_prefix="Hướng 2 – Thay đổi horizon dự báo: ")
    bullet(doc, "Bổ sung giai đoạn thị trường đi ngang hoặc giảm giá, ví dụ "
                "2013 – 2018, để kiểm định tính bền vững của kết luận so sánh "
                "qua các chế độ thị trường khác nhau.",
           bold_prefix="Hướng 3 – Mở rộng giai đoạn kiểm định: ")
    bullet(doc, "Áp dụng kiểm định Jobson – Korkie có hiệu chỉnh Memmel hoặc "
                "bootstrap cho chênh lệch tỷ số Sharpe, và báo cáo Deflated "
                "Sharpe Ratio để hiệu chỉnh thiên lệch lựa chọn.",
           bold_prefix="Hướng 4 – Kiểm định thống kê: ")
    bullet(doc, "Bổ sung cơ chế quản lý khối lượng vị thế tỷ lệ nghịch với biến "
                "động thay vì vị thế toàn phần hoặc bằng không.",
           bold_prefix="Hướng 5 – Quản lý vị thế: ")
    bullet(doc, "Kiểm chứng tính khái quát của kết luận bằng cách áp dụng cùng "
                "quy trình cho bạc, dầu thô và các chỉ số chứng khoán.",
           bold_prefix="Hướng 6 – Mở rộng sang tài sản khác: ")

    heading(doc, "3. Kiến nghị về ứng dụng vào thực tiễn", level=3)
    para(doc,
         "Đối với nhà đầu tư cá nhân, kiến nghị không sử dụng mô hình học máy "
         "làm tín hiệu giao dịch duy nhất khi chưa kiểm định mức độ hiệu chuẩn "
         "của đầu ra xác suất. Kết quả nghiên cứu cho thấy một mô hình có độ "
         "chính xác tổng thể cao vẫn có thể gần như không có năng lực dự báo ở "
         "một phần đáng kể các quan sát. Việc áp dụng bộ lọc độ tin cậy nên được "
         "coi là bước bắt buộc chứ không phải tùy chọn.")
    para(doc,
         "Đối với các tổ chức triển khai giao dịch tự động, kiến nghị đưa việc "
         "tính chi phí giao dịch và benchmark nắm giữ thụ động vào quy trình đánh "
         "giá bắt buộc. Một chiến lược không vượt được benchmark thụ động sau chi "
         "phí thì không tạo ra giá trị kinh tế, bất kể độ chính xác dự báo cao "
         "đến đâu.")

    heading(doc, "4. Kiến nghị về phương pháp nghiên cứu trong lĩnh vực", level=3)
    para(doc,
         "Từ kinh nghiệm thực hiện đề tài, nhóm kiến nghị ba nguyên tắc phương "
         "pháp cho các nghiên cứu ứng dụng học máy trong tài chính. Một là luôn "
         "kiểm định chất lượng dữ liệu đầu vào bằng các đặc tính thống kê đã được "
         "xác lập của chuỗi giá tài chính, trước khi diễn giải bất kỳ kết quả dự "
         "báo nào. Hai là luôn sử dụng thiết kế kiểm định tôn trọng thứ tự thời "
         "gian, không dùng kiểm định chéo ngẫu nhiên. Ba là luôn chuyển kết quả "
         "dự báo thành hiệu quả giao dịch có tính chi phí và đối chiếu với "
         "benchmark thụ động, thay vì chỉ báo cáo các chỉ số phân loại.")


def tai_lieu_tham_khao(doc):
    """3.12. Tai lieu tham khao."""
    heading(doc, "TÀI LIỆU THAM KHẢO", level=1, align="center",
            page_break=True)

    para(doc, "Tài liệu tiếng Anh", bold=True, first_line=0, space_after=6)

    refs = [
        "Appel, G. (1979). The Moving Average Convergence-Divergence Trading "
        "Method. Signalert Corporation, Great Neck, New York.",

        "Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio: "
        "Correcting for Selection Bias, Backtest Overfitting, and Non-Normality. "
        "Journal of Portfolio Management, 40(5), 94–107.",

        "Brier, G. W. (1950). Verification of Forecasts Expressed in Terms of "
        "Probability. Monthly Weather Review, 78(1), 1–3.",

        "Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting "
        "System. Proceedings of the 22nd ACM SIGKDD International Conference on "
        "Knowledge Discovery and Data Mining (KDD '16), 785–794.",

        "Engle, R. F. (1982). Autoregressive Conditional Heteroskedasticity with "
        "Estimates of the Variance of United Kingdom Inflation. Econometrica, "
        "50(4), 987–1008.",

        "Fama, E. F. (1970). Efficient Capital Markets: A Review of Theory and "
        "Empirical Work. Journal of Finance, 25(2), 383–417.",

        "Jobson, J. D., & Korkie, B. M. (1981). Performance Hypothesis Testing "
        "with the Sharpe and Treynor Measures. Journal of Finance, 36(4), "
        "889–908.",

        "Lo, A. W. (2004). The Adaptive Markets Hypothesis: Market Efficiency "
        "from an Evolutionary Perspective. Journal of Portfolio Management, "
        "30(5), 15–29.",

        "Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting "
        "Model Predictions. Advances in Neural Information Processing Systems 30 "
        "(NeurIPS 2017), 4765–4774.",

        "Mandelbrot, B. (1963). The Variation of Certain Speculative Prices. "
        "Journal of Business, 36(4), 394–419.",

        "Memmel, C. (2003). Performance Hypothesis Testing with the Sharpe "
        "Ratio. Finance Letters, 1(1), 21–23.",

        "Murphy, J. J. (1999). Technical Analysis of the Financial Markets: A "
        "Comprehensive Guide to Trading Methods and Applications. New York "
        "Institute of Finance, New York.",

        "Sharpe, W. F. (1966). Mutual Fund Performance. Journal of Business, "
        "39(1), 119–138.",

        "Sortino, F. A., & Price, L. N. (1994). Performance Measurement in a "
        "Downside Risk Framework. Journal of Investing, 3(3), 59–64.",

        "Wilder, J. W. (1978). New Concepts in Technical Trading Systems. Trend "
        "Research, Greensboro, North Carolina.",
    ]
    for i, r in enumerate(refs, start=1):
        p = para(doc, f"[{i}]  {r}", align="justify", first_line=0,
                 space_after=6)
        p.paragraph_format.left_indent = None

    para(doc, "Nguồn dữ liệu", bold=True, first_line=0, space_before=10,
         space_after=6)
    para(doc, "[16]  Bộ dữ liệu giá vàng do đề tài cung cấp: "
              "gold_price_2015_2025_cleaned.csv, giai đoạn 02/01/2015 – "
              "30/12/2025.", align="justify", first_line=0, space_after=6)
    para(doc, "[17]  Yahoo Finance. Dữ liệu giá hợp đồng vàng tương lai COMEX "
              "(mã GC=F), giai đoạn 2015 – 2025. Truy cập qua thư viện yfinance.",
         align="justify", first_line=0, space_after=6)


def phu_luc(doc):
    """3.13. Phu luc."""
    heading(doc, "PHỤ LỤC", level=1, align="center", page_break=True)

    heading(doc, "Phụ lục 1. Cấu trúc chương trình và dữ liệu", level=2)
    para(doc,
         "Toàn bộ mã nguồn và kết quả của đề tài được tổ chức theo cấu trúc thư "
         "mục sau, bảo đảm khả năng tái lập kết quả.")

    table(doc,
          caption_title="Danh mục chương trình của đề tài",
          headers=["Tên chương trình", "Chức năng"],
          rows=[
              ["check_data_quality.py",
               "Thực hiện ba phép kiểm định chất lượng dữ liệu (mục 2.2)"],
              ["ai_vs_ta_original_data.py",
               "Pipeline chính: xây dựng đặc trưng, huấn luyện walk-forward, "
               "ablation study, backtest tám chiến lược, diễn giải mô hình"],
              ["phan_tich_xac_suat.py",
               "Phân tích đầu ra xác suất và mức độ hiệu chuẩn (mục 3.4)"],
              ["download_gold_data.py",
               "Thu thập dữ liệu đối chứng từ nguồn độc lập (mục 3.7)"],
              ["strategy_comparison.py",
               "Thực hiện lại toàn bộ quy trình trên dữ liệu đối chứng (mục 3.7)"],
          ],
          widths=[2.6, 5.4],
          font_size=10,
          note="Nguồn: sản phẩm của nhóm nghiên cứu.")

    table(doc,
          caption_title="Danh mục file kết quả",
          headers=["Nhóm", "File kết quả"],
          rows=[
              ["Bảng số liệu\n(bộ dữ liệu đề tài)",
               "ket_qua_so_sanh_original.csv, ablation_original.csv, "
               "feature_importance_original.csv, loi_nhuan_theo_nam_original.csv, "
               "chi_tieu_on_dinh_original.csv, chi_tiet_xac_suat_du_bao.csv, "
               "bang_hieu_chuan.csv, do_chinh_xac_theo_tu_tin.csv"],
              ["Biểu đồ\n(bộ dữ liệu đề tài)",
               "hinh1_equity_drawdown_original.png, "
               "hinh2_risk_return_original.png, hinh3_loi_nhuan_nam_original.png, "
               "hinh4_ablation_original.png, hinh5_shap_original.png, "
               "hinh6_confusion_matrix_original.png, "
               "hinh7_hieu_chuan_xac_suat.png"],
              ["Dữ liệu đối chứng",
               "strategy_comparison_results.csv, strategy_yearly_returns.csv, "
               "strategy_comparison_equity.png, strategy_risk_return.png, "
               "strategy_yearly_returns.png"],
          ],
          widths=[2.2, 5.8],
          font_size=9,
          note="Nguồn: sản phẩm của nhóm nghiên cứu.")

    heading(doc, "Phụ lục 2. Tổng hợp công thức sử dụng trong đề tài", level=2)

    table(doc,
          caption_title="Tổng hợp các công thức chính",
          headers=["Đại lượng", "Công thức"],
          rows=[
              ["Log-return", "r(t) = ln[ P(t) / P(t−1) ]"],
              ["Biến mục tiêu", "y(t) = 1 nếu r(t+1) > 0; ngược lại y(t) = 0"],
              ["Trung bình động", "MA(n) = [ P(t) + … + P(t−n+1) ] / n"],
              ["Trung bình động hàm mũ",
               "EMA(n)(t) = α·P(t) + (1−α)·EMA(n)(t−1), α = 2/(n+1)"],
              ["Chỉ số sức mạnh tương đối",
               "RSI = 100 − 100/(1 + RS), RS = AvgGain/AvgLoss"],
              ["MACD", "MACD = EMA12 − EMA26; Signal = EMA9(MACD)"],
              ["Độ rộng dải Bollinger", "BB_width = 4σ(20) / MA20"],
              ["Vị trí trong dải Bollinger", "BB_pctB = (z + 2)/4"],
              ["Hàm mất mát log-loss",
               "l(y,p) = −[ y·ln(p) + (1−y)·ln(1−p) ]"],
              ["Gradient và Hessian", "g = p − y;  h = p(1−p)"],
              ["Trọng số lá tối ưu", "w* = −G / (H + λ)"],
              ["Gain của phép chia",
               "Gain = ½[ G_L²/(H_L+λ) + G_R²/(H_R+λ) − G²/(H+λ) ] − γ"],
              ["Chuyển sang xác suất", "P = 1 / (1 + e^(−F))"],
              ["Mức tự tin", "Confidence = max(P, 1−P)"],
              ["Lợi nhuận chiến lược", "r_strat(t) = position(t−1) · r(t)"],
              ["Chi phí giao dịch",
               "cost(t) = |position(t) − position(t−1)| · bps/10.000"],
              ["Đường giá trị tài sản", "E(t) = exp[ Σ r_net(i) ]"],
              ["Tỷ số Sharpe", "Sharpe = [ mean(s)/std(s) ] · √P"],
              ["Tỷ số Sortino",
               "Sortino = [ mean(s)/DownsideStd ] · √P"],
              ["Mức sụt giảm tối đa",
               "MaxDD = min[ E(t)/max{E(1..t)} − 1 ]"],
              ["Tỷ số Calmar", "Calmar = CAGR / |MaxDD|"],
          ],
          widths=[2.6, 5.4],
          font_size=10,
          note="Nguồn: tổng hợp của nhóm nghiên cứu.")

    heading(doc, "Phụ lục 3. Tham số cấu hình thực nghiệm", level=2)
    table(doc,
          caption_title="Tham số cấu hình sử dụng trong thực nghiệm",
          headers=["Tham số", "Giá trị", "Ghi chú"],
          rows=[
              ["Hệ số quy đổi năm (P)", "365",
               "Khớp tần số quan sát thật của chuỗi dữ liệu (mục 2.7)"],
              ["Chi phí giao dịch", "2 bps", "Mỗi lần đổi vị thế"],
              ["Tập huấn luyện ban đầu", "1.825 quan sát", "Khoảng 5 năm"],
              ["Chu kỳ tái huấn luyện", "365 quan sát", "Khoảng 1 năm"],
              ["Ngưỡng phân loại cơ bản", "0,50", "Chiến lược AI_XGB_LongFlat"],
              ["Ngưỡng bộ lọc tin cậy", "0,60", "Chiến lược AI_XGB_Conf60"],
              ["Số quan sát ngoài mẫu", "2.141", "19/02/2020 – 29/12/2025"],
              ["Random seed", "42", "Bảo đảm tái lập kết quả"],
          ],
          widths=[2.6, 1.8, 3.6],
          font_size=10,
          note="Nguồn: thiết kế của nhóm nghiên cứu.")
