#!/usr/bin/env python
# -*- coding: utf8 -*-
import six

left_brackets_ch = '([{'
right_brackets_ch = ')]}'
quotes_ch = '"\''


def str_format(obj, indent=4, fold=True, comma_count_th=30, keep_str=True):
    """
    indent: 缩进长度
    flod: 是否折叠(连续多行时隐藏comma_count_th行之后的数据)
    keep_str: 是否保持字符串原格式
    """
    res = ''
    str_raw = obj if isinstance(obj, six.string_types) else str(obj)
    deep = 0
    last_ch = ''
    comma_count = 0
    not_folding = True
    is_in_str = False
    for ch in str_raw:
        # 保持字符串原格式
        if keep_str:
            if ch in quotes_ch:
                is_in_str = not is_in_str
            if is_in_str:
                if not_folding:
                    res += ch
                continue
        if ch in right_brackets_ch:
            deep -= 1
            res += '\n'
            res += ' ' * deep * indent
            comma_count = 0
        if last_ch == ',' and ch == ' ':
            last_ch = ch
            continue
        if fold:
            if comma_count >= comma_count_th:
                if not_folding:
                    res += '(fold)...'
                not_folding = False
            else:
                not_folding = True
        if not_folding:
            res += ch
        if ch in left_brackets_ch:
            deep += 1
            res += '\n'
            res += ' ' * deep * indent
            comma_count = 0
        if ch == ',':
            comma_count += 1
            if not_folding:
                res += '\n'
                res += ' ' * deep * indent
        last_ch = ch
    return res


def pprint(obj, *args, **kvarg):
    print(str_format(obj, *args, **kvarg))


pp = str_format


def main():
    test_str = """GoodsSpuResult(label=1, debug_info=DebugInfo(scores={'final_score': 0.9820922613143921, 'match_res': 1.0, 'imgs_max_score': 1.0000000000000004, 'imgs_avg_score': 0.9876792259814628, 'bert_score': 0.9558603763580322, 'kv_score': 0.86, 'origin_score': 0.9820922613143921}, filter_detail='[{"name": "适用人群", "prop1": null, "prop2": null, "rule": "soft_part", "label": "匹配"}, {"name": "货号", "prop1": "97a", "prop2": "97a", "rule": "soft_part", "label": "匹配"}, {"name": "品牌", "prop1": "华生||wahson||wahson/华生", "prop2": "wahson||华生||wahson/华生", "rule": "hard_part", "label": "匹配"}, {"name": "尺寸", "prop1": null, "prop2": null, "rule": "soft_part", "label": "匹配"}, {"name": "套装", "prop1": "单品", "prop2": "单品", "rule": "soft_part", "label": "匹配"}, {"name": "套装详情", "prop1": null, "prop2": null, "rule": "hard_part", "label": "匹配"}, {"name": "商品名称", "prop1": null, "prop2": null, "rule": "soft_part", "label": "匹配"}, {"name": "商品", "prop1": "破壁机", "prop2": "破壁机", "rule": "", "label": ""}, {"name": "props_brand", "prop1": "wahson/华生", "prop2": "wahson/华生", "rule": "", "label": ""}, {"name": "props_brand_en", "prop1": "wahson", "prop2": "wahson", "rule": "", "label": ""}, {"name": "产品功能", "prop1": "破壁", "prop2": "破壁", "rule": "", "label": ""}, {"name": "title_产品功能", "prop1": "破壁", "prop2": "破壁", "rule": "", "label": ""}, {"name": "title_商品", "prop1": "破壁机", "prop2": "破壁机", "rule": "", "label": ""}, {"name": "props_brand_zh", "prop1": "华生", "prop2": "华生", "rule": "", "label": ""}, {"name": "发行国家", "prop1": "国行", "prop2": "", "rule": "", "label": ""}, {"name": "props_发行国家", "prop1": "国行", "prop2": "", "rule": "", "label": ""}, {"name": "销量卖点", "prop1": "", "prop2": "热销", "rule": "", "label": ""}, {"name": "title_销量卖点", "prop1": "", "prop2": "热销", "rule": "", "label": ""}]', info1=Product(product_base=ProductBase(product_id=6947596360640135424, platform=1, outer_id='3473808550965420706', name='清清老师优选-华生破壁机', status=2, is_verified=0, discount_price=99900, market_price=199900, pics=['https://sf3-ttcdn-tos.pstatp.com/obj/temai/e0a9e18d70bd2b345a1ef3aaf000ae6dwww800-800', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/d22bac7cd689e69cbf6ec680ae187e8dwww800-800', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/0f6be5fa4daf430043a0d843bca36bd7www800-800', 'https://sf3-ttcdn-tos.pstatp.com/obj/temai/ec10f9e24ade2fb806b9ea63430dc6ddwww800-800', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/7b142a5dbae75c22124de45934acc418www800-800'], info_pics=['https://sf1-ttcdn-tos.pstatp.com/obj/temai/27d8eb80f6559c51638ce827d51b6929www790-1008', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/394c134393350edc7e3410c71f76c25fwww790-346', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/2cdd2563ce76968474223f6f7eaf5e87www790-874', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/84e4faa1bc7e766a78eef816d5b24607www790-802', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/309f9e0c231440c64372a54760cf257fwww790-1226', 'https://sf3-ttcdn-tos.pstatp.com/obj/temai/3a3c3787d5bdb9497da15052826e25c2www790-1069', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/00a16d3c3dbce93a6139968ceb58c009www790-1101', 'https://sf3-ttcdn-tos.pstatp.com/obj/temai/904139477f0bbf5182fa9d3a559267a2www790-876'], outer_url='https://haohuo.jinritemai.com/views/product/item2?id=3473808550965420706', product_type=0, goods_type=5, create_time=1617618161, update_time=1625023237, xd_status=1, xd_check_status=1), product_extra=ProductExtra(spu_id=3473808550965420706, cate_id=21104, first_cate_id=20065, second_cate_id=21104, third_cate_id=0, fourth_cate_id=0, cate_name=None, product_format='{"CCC证书编号":"2019010713196501","产地":"中国大陆","品牌":"wahson/华生","型号规格":"97A","生产厂家":"华生"}', recommend_remark='', skus=[], price_update_time=None, member_price=None, coupon_price=None, group_price=None, mining_price=None, business_price=None, ocr_price=None, normalized_price=None, coupon_infos=None, pic_date=None, carousel_pics=None, cover_pics=None, tags=None, sku_ids=None, props=None, sku_props=None), product_shop=ProductShop(shop_id=8007170, shop_name=None), product_brand=ProductBrand(brand_id=692435121, brand_name=None, source_brand_name=None), product_comment=None, product_order=None, product_feature=None), info2=Product(product_base=ProductBase(product_id=6967519847950369065, platform=1, outer_id='3483771376727398859', name='【热销】华生97A破壁机', status=1, is_verified=1, discount_price=99900, market_price=199900, pics=['https://sf1-ttcdn-tos.pstatp.com/obj/temai/e0a9e18d70bd2b345a1ef3aaf000ae6dwww800-800', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/d22bac7cd689e69cbf6ec680ae187e8dwww800-800', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/0f6be5fa4daf430043a0d843bca36bd7www800-800', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/ec10f9e24ade2fb806b9ea63430dc6ddwww800-800', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/7b142a5dbae75c22124de45934acc418www800-800'], info_pics=['https://sf1-ttcdn-tos.pstatp.com/obj/temai/27d8eb80f6559c51638ce827d51b6929www790-1008', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/394c134393350edc7e3410c71f76c25fwww790-346', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/2cdd2563ce76968474223f6f7eaf5e87www790-874', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/84e4faa1bc7e766a78eef816d5b24607www790-802', 'https://sf1-ttcdn-tos.pstatp.com/obj/temai/309f9e0c231440c64372a54760cf257fwww790-1226', 'https://sf3-ttcdn-tos.pstatp.com/obj/temai/3a3c3787d5bdb9497da15052826e25c2www790-1069', 'https://sf3-ttcdn-tos.pstatp.com/obj/temai/00a16d3c3dbce93a6139968ceb58c009www790-1101', 'https://sf6-ttcdn-tos.pstatp.com/obj/temai/904139477f0bbf5182fa9d3a559267a2www790-876'], outer_url='https://haohuo.jinritemai.com/views/product/item2?id=3483771376727398859', product_type=0, goods_type=5, create_time=1622257463, update_time=1625187293, xd_status=0, xd_check_status=3), product_extra=ProductExtra(spu_id=3483771376727398859, cate_id=21104, first_cate_id=20065, second_cate_id=21104, third_cate_id=0, fourth_cate_id=0, cate_name=None, product_format='{"CCC证书编号": "2019010713196501", "品牌": "wahson/华生", "型号规格": "97A", "生产厂家": "华生"}', recommend_remark='', skus=[], price_update_time=None, member_price=None, coupon_price=None, group_price=None, mining_price=None, business_price=None, ocr_price=None, normalized_price=None, coupon_infos=None, pic_date=None, carousel_pics=None, cover_pics=None, tags=None, sku_ids=None, props=None, sku_props=None), product_shop=ProductShop(shop_id=16698881, shop_name=None), product_brand=ProductBrand(brand_id=692435121, brand_name=None, source_brand_name=None), product_comment=None, product_order=None, product_feature=None), extra={'reason': '融合模型'}), status_code=0)"""
    pprint(test_str)


if __name__ == '__main__':
    main()
