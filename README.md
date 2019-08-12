# Sử dụng api để add host trên zabbix server

Nếu bạn muốn add host lên zabbix server để thực hiện giám sát. Thông thường ta sẽ lên web để thực hiện việc này. Nhưng trong trường hợp ta có rất nhiều host cần phải add thì việc thực hiện trên web sẽ mất rất nhiều thời gian. Chính vì vậu chúng ta có thể sử api để làm việc này một cách đơn giản hơn.

## Chuẩn bị một trường

**Cài đặt python**

```
yum install -y https://centos7.iuscommunity.org/ius-release.rpm

yum update

yum install -y python36u python36u-libs python36u-devel python36u-pip
```

**Tạo virtual environments**

```
python3.6 -m pip install --user virtualenv

python3.6 -m venv venv_zabbix

source venv_zabbix/bin/activate

pip install requests
```

## Download script


## Khai báo các host

Khi bạn download thư mục về trong thư mục sẽ gồm các file `hosts` `main.py` `setting` `zabbix.py`

Trước tiên bạn thực hiện khai báo các host trong muốn thực hiện add trong file `hosts`

Thực hiện khai báo host trong file `hosts` cần khai báo đúng định dạng ("name", "address") ví dụ như sau:

```
("host_1", "192.168.1.2")
("host_2", "192.168.1.3")
("client_3", "10.10.10.10")
```

Lưu ý mỗi dòng chỉ khai báo một địa chỉ và một host name

## Khai báo thông tin của zabbix server 

Thực hiện khai báo thông tin của zabbix server trong file `setting`

```
[zabbix]
zabbix_addr = 192.168.1.1
zabbix_username = admin
zabbix_password = zabbix
group_name = Linux servers
template_name = Template OS Linux
```

Trong đó:
 * zabbix_addr: địa chỉ của zabbix server
 * zabbix_username: user để login zabbix server (trên web)
 * zabbix_passwd: password dùng để login zabbix server (trên web)
 * group_name: tên group bạn muốn add các host đó vào(chú ý viết đúng tên group giống trên web)
 * template_name: tên template mà ta muốn sử dụng cho các host (chú ý viết đúng tên giống trên web)

## Chạy chương trình

```
python main.py
```