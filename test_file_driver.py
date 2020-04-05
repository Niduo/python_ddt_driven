# -*- coding: utf-8 -*-
"""
by: 老屋
des: 文件是json或者yaml格式数据批量读取执行
"""

from selenium import webdriver
from ddt import ddt, file_data
from selenium.common.exceptions import NoSuchElementException
import HTMLTestRunner
import unittest
import time
import logging, traceback
import public_var

caseName = 'fileDriver'
filePath = public_var.file_dir+'\data.json'
report_file = public_var.currentPath+'\\report\\'+caseName+public_var.nowTime+'.html'

print("*"*20, caseName, '', report_file, "*"*20)


# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %Y-%m-%d %H:%M:%S',
    filemode='w',
    filename=public_var.currentPath+'/log/'+public_var.nowTime+'.txt'
)


@ddt
class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('\n', public_var.nowTime)

    def setUp(self):
        self.wd = webdriver.Chrome()
        self.wd.maximize_window()
        self.wd.implicitly_wait(5)
        self.wd.get("https://www.baidu.com")

    def tearDown(self):
        self.wd.close()

    @classmethod
    def tearDownClass(cls):
        print('\n', public_var.nowTime)

    def search_key(self, key):
        self.wd.find_element_by_id("kw").send_keys(key)
        self.wd.find_element_by_id("su").click()

    @file_data(filePath)
    def test_bd_search(self, keys):
        """
        描述： 启动浏览器输入关键字并检查结果
        步骤：
        1、启动浏览器输入打开百度，在json文件获取第一个key ‘python’，输入并搜索
        2、启动浏览器输入打开百度，在json文件获取第一个key ‘java’，输入并搜索
        :param keys: 依次再file_data里读取的value值， 文件key值需保持一致
        :return: 浏览器title=搜索的关键字+_百度搜索
        """

        try:
            self.search_key(keys)
            time.sleep(2)
            expect = keys+"_百度搜索"
            actual = self.wd.title
            self.assertEqual(actual, expect, msg='title error')
        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
            print(e)
        except AssertionError as e:
            logging.info(u"搜索%s, 期望%s" % (actual, expect))
            print(e)
        except Exception as e:
            logging.error(u'未知错误信息'+traceback.format_exc())
            print(e)
        else:
            print('实际值是：', self.wd.title, '期望值:', keys + "_百度搜索")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(TestFile())
    load = unittest.TestLoader()
    suite.addTest(load.loadTestsFromTestCase(TestFile))
    # suite.addTest(TestFile())
    # unittest.TextTestRunner.run(suite)
    # suite = unittest.defaultTestLoader.discover(start_dir='./', pattern=caseFile)
    with open(report_file, 'wb+') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="测试json格式驱动", description="ddt json数据驱动demo")
        runner.run(suite)
