

**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**   
\-----◻◻◻◻◻-----

# 

# **BÁO CÁO** 

#  

# **DỰ ÁN: Khai phá hành vi và độ tin cậy của người dùng thông qua phân tích đánh giá sản phẩm trên sàn amazon**

**Môn học: Khai phá dữ liệu lớn**

**Nhóm môn học : 02**  
***Nhóm bài tập : 05***    
***Giảng viên hướng dẫn: TS.Đặng Hoàng Long***   
***Danh sách thành viên nhóm:***  
*Thái Đức Huy 			MSV: B22DCKH053*

*Trần Tiểu Long	   		MSV: B22DCKH073*

*Nguyễn Đức Mạnh		MSV: B22DCKH075*

  *Lương Minh Quý		MSV: B22DCKH099*

**Hà Nội, tháng 2-2026**

**MỤC LỤC**

[**1\. Giới Thiệu Vấn Đề	2**](#1.-giới-thiệu-vấn-đề)

[**2\. Dataset và Cấu Trúc Dữ Liệu	2**](#2.-dataset-và-cấu-trúc-dữ-liệu)

[2.1. Giới Thiệu Dataset Amazon Reviews 2023	2](#2.1.-giới-thiệu-dataset-amazon-reviews-2023)

[2.2. Phân Tích Cấu Trúc Data	3](#2.2.-phân-tích-cấu-trúc-data)

[**3\. Phương Pháp và Công Cụ (Workflow)3.1. Thư Viện PySpark	5**](#3.-phương-pháp-và-công-cụ-\(workflow\))

[**4\. Mục Tiêu và Kết Quả Kỳ Vọng	6**](#4.-mục-tiêu-và-kết-quả-kỳ-vọng)

[**5\. Tài Liệu Tham Khảo	6**](#5.-tài-liệu-tham-khảo)

# 

## 1\. Giới Thiệu Vấn Đề {#1.-giới-thiệu-vấn-đề}

Trong bối cảnh thương mại điện tử phát triển mạnh mẽ, các nền tảng như Amazon ngày càng phụ thuộc vào đánh giá (reviews) của người dùng để xây dựng lòng tin và hỗ trợ quyết định mua sắm. Tuy nhiên, vấn đề đánh giá giả mạo (fake reviews) đang trở thành thách thức lớn, ảnh hưởng đến tính minh bạch và công bằng của hệ thống.  
Theo các nghiên cứu khảo sát, fake reviews có thể chiếm tỷ lệ đáng kể trong các đánh giá trực tuyến, dẫn đến việc thao túng xếp hạng sản phẩm, giảm lòng tin của người tiêu dùng và gây thiệt hại kinh tế lên đến hàng tỷ đô la mỗi năm. Các hành vi như "seeding" (buff điểm ảo) từ các "click farm" hoặc bot tự động không chỉ làm méo mó dữ liệu mà còn ảnh hưởng đến hệ thống khuyến nghị (recommendation systems).  
Đề tài "Khai phá hành vi và độ tin cậy của người dùng thông qua phân tích đánh giá sản phẩm trên sàn Amazon" nhằm giải quyết vấn đề này bằng cách sử dụng kỹ thuật khai thác dữ liệu (data mining) và học máy (machine learning) để phân tích hành vi người dùng (như tần suất đánh giá, độ lệch rating) và phát hiện đánh giá thiếu tin cậy (dựa trên các đặc trưng như verified purchase, helpful votes). Việc này không chỉ giúp cải thiện chất lượng dữ liệu mà còn hỗ trợ các nền tảng e-commerce trong việc lọc spam, nâng cao trải nghiệm người dùng và bảo vệ doanh nghiệp chân chính.

## 2\. Dataset và Cấu Trúc Dữ Liệu {#2.-dataset-và-cấu-trúc-dữ-liệu}

### 2.1. Giới Thiệu Dataset Amazon Reviews 2023 {#2.1.-giới-thiệu-dataset-amazon-reviews-2023}

Dataset Amazon Reviews 2023 là bộ dữ liệu quy mô lớn được thu thập bởi McAuley Lab tại Đại học California San Diego (UCSD) vào năm 2023, mở rộng từ các phiên bản trước đó. Bộ dữ liệu này bao gồm các đánh giá người dùng, metadata sản phẩm và các liên kết tương tác từ nền tảng Amazon.

* **Quy mô và Phạm vi:**  
  * **Tổng thể:** Hơn 571.54 triệu đánh giá, 54.51 triệu người dùng và 48.19 triệu sản phẩm.  
  * **Phạm vi thời gian:** Từ tháng 5/1996 đến tháng 9/2023.  
  * **Lĩnh vực:** Bao quát 33 danh mục sản phẩm chính (ví dụ: All\_Beauty, Appliances, Books, Electronics, v.v.), cộng thêm một danh mục "Unknown".  
  * **Token:** Khoảng 30.14 tỷ token từ đánh giá và 30.78 tỷ token từ metadata.  
* **Định dạng và Truy cập:**  
  * Dữ liệu được lưu trữ dưới dạng **JSON Lines (.jsonl)** trên Hugging Face Datasets hoặc GitHub, hỗ trợ tải streaming.  
  * So với phiên bản 2014 (142.8 triệu reviews), phiên bản 2023 lớn hơn 245%, với độ chính xác thời gian cao hơn (đơn vị giây) và metadata được làm sạch tốt hơn, phù hợp cho các nhiệm vụ NLP, RecSys và phát hiện fake reviews.

### 2.2. Phân Tích Cấu Trúc Data {#2.2.-phân-tích-cấu-trúc-data}

Dữ liệu được tổ chức thành hai thành phần chính: **User Reviews** (đánh giá người dùng) và **Item Metadata** (metadata sản phẩm). Mỗi thành phần được lưu trữ trong các file riêng biệt theo danh mục sản phẩm (ví dụ: **All\_Beauty.jsonl** cho đánh giá và **meta\_All\_Beauty.jsonl** cho metadata).

* **Tổ chức file**: Có 33 file đánh giá và metadata tương ứng cho từng danh mục. Tổng kích thước khoảng hàng trăm GB, đòi hỏi xử lý dữ liệu lớn (big data).

**Cấu Trúc Chi Tiết Các Trường (Fields)**

* **User Reviews (Đánh Giá Người Dùng)**

| Trường | Kiểu Dữ Liệu | Mô Tả |
| ----- | ----- | ----- |
| rating | float | Đánh giá sao (1.0 đến 5.0) |
| title | str | Tiêu đề đánh giá |
| text | str | Nội dung đánh giá |
| images | list | Danh sách URL hình ảnh (kích thước nhỏ, trung bình, lớn) |
| asin | str | ID sản phẩm biến thể |
| parent\_asin | str | ID sản phẩm cha (dùng để liên kết metadata) |
| user\_id | str | ID người đánh giá |
| timestamp | int | Thời gian Unix (đơn vị giây) |
| verified\_purchase | bool | Xác thực mua hàng (True/False) |
| helpful\_votes | int | Số lượt bình chọn hữu ích |
| sort\_timestamp | int | Thời gian sắp xếp (đơn vị mili giây) |


  


  


* **Item Metadata (Metadata Sản Phẩm)**

| Trường | Kiểu Dữ Liệu | Mô Tả |
| ----- | ----- | ----- |
| main\_category | str | Danh mục chính (ví dụ: "All Beauty") |
| title | str | Tên sản phẩm |
| average\_rating | float | Đánh giá trung bình |
| rating\_number | int | Tổng số đánh giá |
| features | list | Danh sách tính năng nổi bật |
| description | list | Mô tả chi tiết (có thể nhiều phần) |
| price | float | Giá USD tại thời điểm thu thập |
| images | list | Danh sách hình ảnh sản phẩm (hi\_res, thumb, large) |
| videos | list | Danh sách video (tiêu đề và URL) |
| store | str | Tên cửa hàng bán |
| categories | list | Danh sách danh mục phân cấp |
| details | dict | Thông số kỹ thuật (key-value, ví dụ: thương hiệu, kích thước) |
| parent\_asin | str | ID sản phẩm cha |
| bought\_together | list | Sản phẩm gợi ý mua kèm |

* **Thống kê tổng quan**

| Chỉ Số | Giá Trị |
| ----- | ----- |
| Tổng Đánh Giá | 571.54 triệu |
| Tổng Người Dùng | 54.51 triệu |
| Tổng Sản Phẩm | 48.19 triệu |
| Token Đánh Giá | 30.14 tỷ |
| Token Metadata | 30.78 tỷ |
| Số Danh Mục | 33 \+ Unknown |

## 3\. Phương Pháp và Công Cụ (Workflow) {#3.-phương-pháp-và-công-cụ-(workflow)}

### 3.1. Thư Viện PySpark

PySpark là giao diện Python cho Apache Spark, một nền tảng xử lý dữ liệu phân tán mạnh mẽ. PySpark cho phép thực hiện các tác vụ xử lý Big Data thời gian thực, phân tán trên nhiều node, sử dụng Python để viết code.  
Các tính năng chính được sử dụng trong dự án:

* **Spark SQL**: Hỗ trợ truy vấn dữ liệu như SQL, phù hợp cho việc lọc và tổng hợp reviews (ví dụ: tính **average\_rating** theo **user\_id**).  
* **DataFrame API**: Xử lý dữ liệu cấu trúc, dễ dàng thực hiện feature engineering (như tính độ lệch rating *RD \= |R\_user \- μ\_product|*).  
* **MLlib**: Thư viện học máy tích hợp cho clustering (K-Means) và anomaly detection (Isolation Forest).  
* **Streaming**: Hỗ trợ xử lý dữ liệu theo luồng, lý tưởng cho dataset lớn như Amazon Reviews mà không cần tải toàn bộ vào RAM.

PySpark được chọn vì khả năng scale ngang (horizontal scaling), tiết kiệm bộ nhớ và tốc độ cao hơn so với Pandas (đến 10x nhanh hơn với dữ liệu TB)

### **3.2. Tổng quan Workflow Dự Án**

Trong workflow, PySpark sẽ được dùng cho các giai đoạn **Ingestion, Cleaning và Engineering** để xử lý dữ liệu phân tán.

| Giai Đoạn | Mục Tiêu Chính | Công Cụ Chủ Đạo | Đầu Ra (Output) |
| ----- | ----- | ----- | ----- |
| **1\. Ingestion** | Thu thập & nạp dữ liệu | Hugging Face Stream, Polars | File Parquet thô (Raw) |
| **2\. Cleaning** | Tiền xử lý & làm sạch | Polars, Regex | File Parquet sạch (Cleaned) |
| **3\. Engineering** | Kỹ nghệ đặc trưng | Window Functions, NLP (VADER/Transformers) | Ma trận đặc trưng (Feature Matrix) |
| **4\. Modeling** | Mô hình hóa & phân tích | K-Means, Isolation Forest, Graph (NetworkX) | Nhãn hành vi & Điểm tin cậy |
| **5\. Insight** | Trực quan hóa & kết luận | Streamlit / Power BI | Dashboard & báo cáo chiến lược |

## 4\. Mục Tiêu và Kết Quả Kỳ Vọng {#4.-mục-tiêu-và-kết-quả-kỳ-vọng}

Dự án nhằm đạt được các mục tiêu sau:

* **Khai phá hành vi người dùng**: Phân loại người dùng thành các nhóm (clusters) như "Khách hàng trung thành," "Người dùng khó tính," và "Người dùng ngẫu hứng," sử dụng K-Means trên các đặc trưng như tần suất review, độ dài text và diversity categories.  
* **Đánh giá độ tin cậy**: Phát hiện đánh giá giả mạo với độ chính xác cao (\>85%) bằng Isolation Forest, dựa trên các chỉ số như verified purchase ratio, helpfulness ratio và anomaly score. Kỳ vọng xác định tỷ lệ fake reviews theo danh mục.  
* **Xây dựng dashboard**: Tạo báo cáo trực quan (Streamlit/Power BI) để hiển thị insights, như correlation giữa độ tin cậy và thời gian/sector, hỗ trợ ra quyết định cho e-commerce.  
* **Tối ưu hóa quy trình**: Xử lý toàn bộ dataset mà không gặp vấn đề tài nguyên, với thời gian xử lý dưới 2 tuần cho full pipeline.

**Kỳ vọng tổng thể**: Đóng góp một mô hình hybrid (behavioral \+ NLP) để cải thiện hệ thống lọc reviews, giảm tỷ lệ fake reviews và nâng cao độ tin cậy dữ liệu trên các nền tảng thương mại điện tử tương tự Amazon.

## 5\. Tài Liệu Tham Khảo {#5.-tài-liệu-tham-khảo}

1. [McAuley-Lab/Amazon-Reviews-2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023). Hugging Face Datasets  
2. [Amazon Reviews'23](https://jmcauley.ucsd.edu/data/amazon_v2/2023/index.html). GitHub Pages.  
3. [Scripts for processing the Amazon Reviews 2023 dataset](https://github.com/McAuley-Lab/Amazon-Reviews-2023). GitHub  
4. [Amazon review data](https://jmcauley.ucsd.edu/data/amazon_v2/). UCSD McAuley Lab.  
5. [Amazon Reviews Data 2023](https://www.kaggle.com/datasets/piterfm/amazon-reviews-data-2023). Kaggle..  
6. [PySpark Overview](https://spark.apache.org/docs/latest/api/python/index.html). Apache Spark Documentation.  
7. [API Reference](https://spark.apache.org/docs/latest/api/python/index.html). Apache Spark PySpark Documentation.   
8. [Spark SQL](https://spark.apache.org/docs/latest/sql-programming-guide.html). Apache Spark PySpark Documentation.   
9. Hajek, P. et al. (2023). Fake review detection in e-Commerce platforms using aspect-based sentiment analysis. *Journal of Business Research*.  
10. [Fake reviews detection in e-commerce using machine learning techniques: A comparative survey](https://www.researchgate.net/publication/349479366_Fake_reviews_detection_in_e-commerce_using_machine_learning_techniques_A_comparative_survey). ResearchGate.  
11. Abdelmohsen, Y. (2024). Fake Reviews Detection Using Deep Learning: A Survey. *IEEE Xplore*.  
12. [Fake Reviews Detection on E-Commerce Websites Using Novel User Behavioral Features: An Experimental Study](https://dl.acm.org/doi/10.1145/3588267.3599971). ACM Digital Library.

