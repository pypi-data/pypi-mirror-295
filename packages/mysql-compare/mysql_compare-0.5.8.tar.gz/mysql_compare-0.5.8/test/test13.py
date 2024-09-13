# if __name__ == "__main__":
#     source_dsn = {"host": "192.168.161.94", "user": "cy", "password": "cy"}
#     target_dsn = {"host": "192.168.161.94", "user": "cy", "password": "cy"}
#     MysqlTableCompare(source_dsn, target_dsn, "merchant_center_ouku_v1", "v3_wh_to_whg", "merchant_center_ouku_v1", "v3_wh_to_whg", 1, 200).run()


import ffff

source_dsn = {"host": "192.168.161.94", "user": "cy", "password": "cy"}
target_dsn = {"host": "192.168.161.94", "user": "cy", "password": "cy"}
ffff.MysqlTableCompare(
    source_dsn,
    target_dsn,
    "merchant_center_ouku_v1",
    "mc_resource_meta",
    "test",
    "mc_resource_meta",
    10000,
).run()
