# 背景メモ
Repository のメソッドを `async def` にしている理由: \
IOバウンドな一連の手続きの最適化余地を広げるため。例えば以下のように、待機時間が長く発生するような処理を並行で処理できるようになる。

```Python
# 大量のデータ読み出し処理
co1 = self.abc_repository.bulk_get(...)
# 外部リソースに対する別の問い合わせ処理
co2 = self.usecase_port.retrieve_xyz_from_ex(...)

abcs = await co1
xyzs = await co2
```