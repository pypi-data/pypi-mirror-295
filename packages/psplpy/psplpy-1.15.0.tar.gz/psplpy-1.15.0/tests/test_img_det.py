from tests.__init__ import *
from psplpy.image_det import *
from psplpy.ocr_utils import *
from tests.test_ocr_utils import run_ocr_server, host


def test_img_det():
    image = rc_dir / 'cat.png'
    template_image = rc_dir / 'det_block.png'

    p = PerfCounter()
    result = ImgDet.get_boxes(image, template_image, confidence=0.8, method=ImgDet.TM_CCOEFF_NORMED,
                              draw_result=tmp_dir / 'det_marked.png', save_match=tmp_dir / 'det_match.png')
    p.show('det')
    print(result)
    result = ImgDet.get_box(image, template_image, confidence=0.8, method=ImgDet.TM_CCOEFF_NORMED,
                            draw_result=tmp_dir / 'det_marked.png', save_match=tmp_dir / 'det_match.png')
    p.show('det')
    print(result)
    assert result == (Rect([(840, 189), (890, 239)], rect_format=Rect.LT_RB), 0.9999983906745911)


def test_txt_det():
    run_ocr_server()
    image = rc_dir / 'ocr.png'
    p = PerfCounter()
    ocr_result = Ocr(host=host).get(image)
    p.show('ocr')
    print(ocr_result)

    def do_noting(txt: str) -> str:
        return txt

    t = TxtDet(txt_processor=TxtProcessor(TxtProcessor.NO_SPACE, TxtProcessor.CASEFOLD, do_noting),
               process_text=True)
    boxes = t.get_boxes(ocr_result, '右上角Test')
    p.show('boxes')
    print(boxes)
    assert boxes == TextInfoList([[Rect([[773.0, 6.0], [992.0, 28.0]]), '我是右上角Test文本', 0.9980501532554626]])
    text = t.get_txt(ocr_result, Rect([[773.0, 6.0], [992.0, 28.0]]))
    p.show('text')
    print(text)
    match_obj = t.match(ocr_result, [[Rect([[773.0, 6.0], [992.0, 28.0]]), '右上角Test', 0.99],
                                     [Rect([[100, 6.0], [200, 28.0]]), 'mismatch文本', 0.99]], confidence=0.5)
    p.show('match_obj')
    assert (match_obj.bool, match_obj.result_list, match_obj.confidence) == (True, [True, False], 0.5)
    assert match_obj.match_list == [[Rect([[773.0, 6.0], [992.0, 28.0]]), '右上角Test', 0.99]]
    assert match_obj.mismatch_list == [[Rect([[100, 6.0], [200, 28.0]]), 'mismatch文本', 0.99]]


def tests():
    test_img_det()
    test_txt_det()


if __name__ == '__main__':
    tests()
