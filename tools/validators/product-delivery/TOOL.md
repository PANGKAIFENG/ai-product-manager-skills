# Product Delivery Validator

确定性校验 `product-delivery-manifest.yaml` 的结构、证据引用、输入 fingerprint 和状态转移。实现复用 `skills/prd-architect/scripts/validate_product_delivery_manifest.py`，以保持 PRD 单 Skill 安装时仍可运行；此目录是 Tool 目录，不计入原子 Skill。

```bash
python3 skills/prd-architect/scripts/validate_product_delivery_manifest.py <manifest.yaml> --json
```
