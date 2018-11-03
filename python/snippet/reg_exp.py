# -*- coding: utf-8 -*-
# 请尝试写一个验证Email地址的正则表达式。版本一应该可以验证出类似的Email：
# someone@gmail.com
# bill.gates@microsoft.com
import re

def is_valid_email(addr):
    reg_exp = r'^[^-@]+@\w+\.\w+$'
    ret = re.match(reg_exp, addr)
    return bool(ret)

# 版本二可以提取出带名字的Email地址：
# <Tom Paris> tom@voyager.org => Tom Paris
# bob@example.com => bob
def name_of_email(addr):
    reg_exp = r'^(?:<(.+)>)?\s*([^-@]+)@\w+\.\w+$'
    ret = re.match(reg_exp, addr)
    if ret is None:
        return False
    else:
        return ret.group(1) or ret.group(2)


if __name__ == '__main__':
    # 测试:
    assert is_valid_email('someone@gmail.com')
    assert is_valid_email('bill.gates@microsoft.com')
    assert not is_valid_email('bob#example.com')
    assert not is_valid_email('mr-bob@example.com')
    print('is_valid_email ok')

    assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
    assert name_of_email('tom@voyager.org') == 'tom'
    print('name_of_email ok')
