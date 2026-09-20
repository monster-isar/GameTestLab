import pytest
from gacha.corev1 import read_config,do_gacha
from pathlib import Path

gacha_dir=Path(__file__).resolve().parent.parent
def test_gacha_count():
    pool,tier_ids,levels,base_weight,weight,tier1,tier2=read_config(gacha_dir/"gacha")
    count=100
    result_gacha=do_gacha(pool,tier_ids,levels,base_weight,weight,tier1,tier2,gacha_dir/"gacha"/"results.txt",count)
    assert count==len(result_gacha)
#测试抽卡逻辑：抽卡结果的记录次数是否与指定的抽卡次数相等

@pytest.mark.parametrize(
        "input_invalid,except_error",
        [
            (-5,None),
            ("a",ValueError),
            (0.4,ValueError),
            ([3,1],ValueError),
            ("abc",ValueError)
        ]
    )
@pytest.mark.xfail(reason="未对输入<0或输入其他类型的情况做异常处理")
def test_gacha_invalid_count(input_invalid,except_error):
    pool,tier_ids,levels,base_weight,weight,tier1,tier2=read_config(gacha_dir/"gacha")
    if except_error:
        with pytest.raises(except_error):
            do_gacha(pool,tier_ids,levels,base_weight,weight,tier1,tier2,gacha_dir/"gacha"/"results.txt",input_invalid)
    else:
        assert do_gacha(pool,tier_ids,levels,base_weight,weight,tier1,tier2,gacha_dir/"gacha"/"results.txt",input_invalid) is True
#测试输入异常：抽卡输入的数字<0时是否抛出异常、输入字符时是否抛出异常