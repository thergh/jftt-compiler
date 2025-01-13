#! /bin/sh

echo; echo "================== error1.imp =================="
python3 src/kompilator.py tests/error1.imp code/error1.mr
echo; echo "================== error2.imp =================="
python3 src/kompilator.py tests/error2.imp code/error2.mr
echo; echo "================== error3.imp =================="
python3 src/kompilator.py tests/error3.imp code/error3.mr
echo; echo "================== error4.imp =================="
python3 src/kompilator.py tests/error4.imp code/error4.mr
echo; echo "================== error5.imp =================="
python3 src/kompilator.py tests/error5.imp code/error5.mr
echo; echo "================== error6.imp =================="
python3 src/kompilator.py tests/error6.imp code/error6.mr
echo; echo "================== error7.imp =================="
python3 src/kompilator.py tests/error7.imp code/error7.mr
echo; echo "================== error8.imp =================="
python3 src/kompilator.py tests/error8.imp code/error8.mr