# -*- coding: utf-8 -*-
"""
by: 老屋
des: web测试， data数据参数化驱动, 分别为list,, tuples, dict
"""
from selenium import webdriver
from ddt import ddt, data, unpack
from selenium.common.exceptions import NoSuchElementException
import HTMLTestRunner
import unittest
import logging, traceback
import public_var
import time

caseName = 'fileDriver'
report_file = public_var.currentPath+'\\report\\'+caseName+public_var.nowTime+'.html'

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %Y-%m-%d %H:%M:%S',
    filemode='w'
)


@ddt
class TestDataDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wd = webdriver.Chrome()
        cls.wd.maximize_window()
        cls.wd.implicitly_wait(5)
        cls.url = "https://www.baidu.com"

    def setUp(self):
        print('\nsetUp start')
        self.wd.get(self.url)

    def tearDown(self):
        print('\ntearDown end')

    @classmethod
    def tearDownClass(cls):
        print('\nteardown class')
        cls.wd.close()

    def search(self, searchWord):
        self.wd.get(self.url)
        self.wd.find_element_by_id("kw").send_keys(searchWord)
        self.wd.find_element_by_id("su").click()
        time.sleep(1)

    @data(["case1", "selenium"], ["case2", "docker"])
    @unpack
    def test_list_search(self, keys, searchWord):
        try:
            print("第一组list测试用例：", keys)
            self.search(searchWord)
            actual = self.wd.title
            expect = searchWord+"_百度搜索"
            self.assertEqual(actual, expect, msg='不存在')
        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
            print(e)
        except AssertionError as e:
            logging.info(u"搜索值%s不在页面中" % searchWord)
            print(e)
        except Exception as e:
            logging.error(u'未知错误信息'+traceback.format_exc())
            print(e)

    @data(("case1", "mouse"), ("case2", "keyboard"))
    @unpack
    # @unittest.skip("暂不执行")
    def test_tuple_search(self, keys, searchWord):
        try:
            self.search(searchWord)
            actual = self.wd.title
            expect = searchWord+'_百度搜索'
            print("第二组元祖测试用例:", keys)
            self.assertEqual(actual, expect, msg='不存在')
        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
            print(e)
        except AssertionError as e:
            logging.info(u"搜索值%s不在页面中" % searchWord)
            print(e)
        except Exception as e:
            logging.error(u'未知错误信息'+traceback.format_exc())
            print(e)

    @data({"keys": "1"}, {"keys": "2"})
    @unpack
    # @unittest.skip("暂不执行")
    def test_dict_search(self, keys):
        try:
            self.search(keys)
            actual = self.wd.title
            expect = keys+'_百度搜索'
            print("第二组元祖测试用例:", keys)
            self.assertEqual(actual, expect, msg='不存在')
        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
            print(e)
        except AssertionError as e:
            logging.info(u"搜索值%s不在页面中" % keys)
            print(e)
        except Exception as e:
            logging.error(u'未知错误信息'+traceback.format_exc())
            print(e)


if __name__ == '__main__':
    suit = unittest.TestSuite()
    load = unittest.TestLoader()
    suit.addTest(load.loadTestsFromTestCase(TestDataDriver))
    # suit.addTest(TestDataDriver('test_list_search'))
    with open(report_file, 'w', encoding='utf-8') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,  title='测试data格式驱动', description='des')
        runner.run(suit)