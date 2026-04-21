# -*- encoding=utf8 -*-
__author__ = "kay"

from airtest.core.api import *

auto_setup(__file__)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

keyevent("HOME")
if poco("设置").exists():
    swipe([843,1376],[103,1572],duration=1.0)
poco("闹钟时钟").wait_for_appearance()
poco("闹钟时钟").click()
keyevent("HOME")
swipe([92,1572],[874,1572],duration=1.0)

poco("android.widget.FrameLayout").offspring("com.bbk.launcher2:id/workspace").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").child("相册精选")[2].child("相册精选").wait_for_appearance()

touch([777,269])
touch([159,879])
time.sleep(2)
keyevent("HOME")