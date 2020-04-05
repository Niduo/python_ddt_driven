# -*- coding: utf-8 -*-
"""
by: 老屋
des: 读取txt文件数据做输入和断言， 并将结果写入一个新的txt
"""
from selenium import webdriver
import public_var
import time

reportFile = public_var.report_dir+'TestTxtDriver'+public_var.nowTime+'.txt'


class TestTxtDriver:
    def __init__(self):
        self.wd = webdriver.Chrome()
        self.wd.maximize_window()
        self.wd.implicitly_wait(5)
        self.test_result = []

    def search_key(self, key):
        self.wd.get("http://www.baidu.com")
        self.wd.find_element_by_id("kw").send_keys(key)
        self.wd.find_element_by_id("su").click()

    def read_txt(self):
        with open('./test_file/data.txt', 'r', encoding='utf-8') as fp:
            line = fp.readlines()
            for i in range(len(line)):
                try:
                    # 用||分割去空格取出入参
                    search_word = line[i].split('||')[0].strip()
                    print(search_word)
                    self.search_key(search_word)
                    time.sleep(5)
                    # 用||分割去空格取出期望结果
                    expect_word = line[i].split('||')[1].strip()
                    assert expect_word in self.wd.page_source
                    self.test_result.append(search_word+'||'+'成功\n')
                except AssertionError as e:
                    print(e, "期望显示的结果：%s：页面中不存在" % expect_word)
                    self.test_result.append(search_word+'||'+'失败\n')
                except Exception as e:
                    print(e)
                    self.test_result.append(search_word+'||'+'出现异常\n')
        self.wd.close()

    def write_result(self):
        with open(reportFile, 'w', encoding='utf-8') as fp:
            fp.writelines(self.test_result)

    def run(self):
        self.read_txt()
        self.write_result()


if __name__ == '__main__':
    t = TestTxtDriver()
    t.run()