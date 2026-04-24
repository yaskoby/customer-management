# スナック向け 顧客管理 + LINE配信管理 + 来店履歴管理ツール 詳細設計書

## 1. 目的

スナック店舗における顧客情報、来店履歴、LINE配信履歴を一元管理し、再来店率向上と店舗運営の属人化解消を実現する。

## 2. 想定利用者

### 2.1 店舗オーナー / ママ

- 顧客全体の把握
- 休眠顧客の掘り起こし
- 売上傾向の確認
- キャストごとの担当状況確認

### 2.2 店長 / 管理者

- 顧客台帳メンテナンス
- 来店登録
- 配信承認
- イベント配信

### 2.3 キャスト

- 担当顧客の確認
- 来店前メモ確認
- 接客後メモ登録
- 個別フォロー対象の確認

## 3. 解決したい業務課題

- 顧客情報が紙や個人LINEに散在している
- 常連の好みや会話履歴がスタッフ間で共有されない
- 来店後のフォローが担当者任せで再現性がない
- しばらく来ていない顧客を掘り起こせない
- イベント告知を一斉送信しているが効果測定できない

## 4. ゴール

- 顧客単位で「基本情報」「来店履歴」「LINE接触履歴」「接客メモ」が見える
- セグメント別にLINE配信できる
- 来店の空き期間に応じた再来店施策を打てる
- 店舗資産として顧客情報を蓄積できる

## 5. 提供範囲

### 5.1 MVP範囲

- 顧客管理
- LINE配信対象管理
- 来店履歴登録
- ボトル管理
- ダッシュボード
- 権限管理
- 基本分析

### 5.2 将来拡張

- LINE webhookによる会話連携
- 予約管理
- 会計システム連携
- 多店舗管理
- AIによる次回接客提案

## 6. 業務要件

### 6.1 顧客管理要件

- 顧客の基本情報を登録できること
- 1顧客に複数の連絡先を保持できること
- LINE友だち連携状態を保持できること
- 好み、NG事項、誕生日、来店頻度を記録できること
- 担当キャストを複数紐づけできること
- 顧客ランクを管理できること
- メモを時系列で追記できること

### 6.2 来店履歴要件

- 来店日時を登録できること
- 同伴有無、来店目的、イベント参加有無を記録できること
- 会計金額とボトル情報を記録できること
- 同席キャストを複数登録できること
- 来店時メモと次回来店促進メモを分けて記録できること

### 6.3 LINE配信要件

- 顧客のLINE配信可否を管理できること
- 一斉配信、セグメント配信、個別配信に対応すること
- 配信テンプレートを保存できること
- 配信実績を顧客単位で確認できること
- 配信対象抽出条件を保存できること

### 6.4 分析要件

- 来店回数
- 最終来店日
- 累計売上
- 月別来店数
- イベント別反応
- キャスト担当別売上
- 休眠顧客一覧

## 7. 非機能要件

### 7.1 性能

- 通常画面表示は3秒以内
- 顧客一覧1,000件規模で実用速度を確保
- LINE一斉配信時は非同期ジョブで処理

### 7.2 可用性

- 営業前後のピーク時間帯でも利用可能
- 日次バックアップ
- 障害時の復旧手順を整備

### 7.3 セキュリティ

- 店舗単位のデータ分離
- ロールベースアクセス制御
- 通信暗号化
- 監査ログ
- 個人情報マスキング

### 7.4 運用性

- スマホ利用前提のUI
- PCでも一括管理しやすい管理画面
- CSV入出力
- 誤操作防止の確認UI

## 8. ユーザーロールと権限

| ロール | 顧客閲覧 | 顧客編集 | 来店登録 | 配信作成 | 配信承認 | 設定変更 |
| --- | --- | --- | --- | --- | --- | --- |
| オーナー | 全件 | 全件 | 可 | 可 | 可 | 可 |
| 店長 | 全件 | 全件 | 可 | 可 | 可 | 一部 |
| キャスト | 担当中心 | 担当中心 | 可 | 個別のみ | 不可 | 不可 |
| 閲覧専用 | 全件 | 不可 | 不可 | 不可 | 不可 | 不可 |

## 9. 主要ユースケース

### 9.1 新規顧客登録

1. 管理者が顧客を登録する
2. 担当キャストを紐づける
3. LINE友だち状況を登録する
4. 初回来店情報を記録する

### 9.2 来店後フォロー

1. 当日の来店者を登録する
2. 接客メモを残す
3. 次回誘導メモを登録する
4. 3日後フォロー対象として抽出する
5. LINE配信または個別連絡を行う

### 9.3 イベント集客

1. 配信対象条件を設定する
2. 対象顧客をプレビューする
3. テンプレートを選択する
4. 配信実行する
5. 反応と来店結果を確認する

## 10. 画面一覧

### 10.1 ログイン

- メールログイン
- パスワード再発行
- 2段階認証オプション

### 10.2 ダッシュボード

- 本日の来店予定
- 最近来ていない顧客
- 誕生日が近い顧客
- 配信結果サマリー
- 売上サマリー

### 10.3 顧客一覧

- 名前検索
- ニックネーム検索
- タグ絞り込み
- LINE連携有無
- 最終来店日
- 担当キャスト

### 10.4 顧客詳細

- 基本情報
- タグ
- 担当情報
- LINE状態
- 来店履歴タイムライン
- 接客メモ
- 配信履歴
- ボトル一覧

### 10.5 来店登録画面

- 顧客選択
- 来店日時
- 同伴情報
- 会計
- 同席キャスト
- メモ

### 10.6 LINE配信画面

- 配信種別選択
- セグメント条件設定
- 配信本文作成
- テンプレート適用
- 配信予約
- 配信結果確認

### 10.7 テンプレート管理

- イベント案内
- 誕生日フォロー
- 休眠掘り起こし
- 来店お礼

### 10.8 設定画面

- 店舗情報
- ユーザー管理
- 権限設定
- LINE接続設定
- マスタ管理

## 11. 顧客詳細画面の情報設計

### 11.1 ヘッダー

- 顧客名
- ニックネーム
- LINE友だち状態
- 最終来店日
- 休眠ステータス
- 担当キャスト

### 11.2 タブ

- 概要
- 来店履歴
- LINE履歴
- ボトル
- メモ
- 分析

### 11.3 重要表示項目

- 誕生日
- 好みの酒
- 好きな曲
- NG話題
- よく来る曜日
- 同伴者傾向
- 次回提案ネタ

## 12. ダッシュボードKPI

- 本日来店予定数
- 今月来店者数
- 今月売上
- 今月新規顧客数
- 最終来店30日超の顧客数
- LINE配信件数
- 配信経由来店件数

## 13. セグメント条件設計

### 13.1 基本条件

- 性別
- 年代
- 誕生月
- 居住エリア
- 職業カテゴリ

### 13.2 来店条件

- 最終来店日
- 来店回数
- 指定期間の来店有無
- イベント参加有無
- 会計金額帯

### 13.3 関係性条件

- 担当キャスト
- 顧客ランク
- 紹介元
- タグ
- ボトル保有有無

### 13.4 配信条件

- LINE連携済み
- 配信許諾済み
- 最近配信したか
- 特定テンプレート送信済みか

## 14. 自動判定ロジック

### 14.1 顧客ランク

- S: 直近90日で3回来店以上かつ累計売上上位
- A: 直近90日で2回来店以上
- B: 直近180日で1回来店以上
- C: それ以外

### 14.2 休眠判定

- 注意: 最終来店21日超
- 休眠: 最終来店45日超
- 長期休眠: 最終来店90日超

### 14.3 フォロー推奨

- 来店翌日: お礼メッセージ候補
- 来店7日後: 再来店打診候補
- 誕生日7日前: バースデー告知候補
- イベント3日前: 対象顧客への告知候補

## 15. データモデル

### 15.1 エンティティ一覧

- tenants
- stores
- users
- roles
- customers
- customer_tags
- tags
- customer_staff_assignments
- visits
- visit_staffs
- bottles
- bottle_keeps
- line_accounts
- line_friend_links
- campaigns
- campaign_targets
- message_templates
- message_deliveries
- customer_notes
- audit_logs

### 15.2 主要テーブル定義

#### tenants

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| name | varchar | テナント名 |
| plan_type | varchar | 契約プラン |
| created_at | timestamptz | 作成日時 |

#### stores

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| name | varchar | 店舗名 |
| phone | varchar | 店舗電話番号 |
| address | text | 住所 |
| timezone | varchar | 既定タイムゾーン |

#### customers

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| store_id | uuid | FK |
| last_name | varchar | 姓 |
| first_name | varchar | 名 |
| nickname | varchar | 呼び名 |
| gender | varchar | 任意 |
| birth_date | date | 任意 |
| phone | varchar | 任意 |
| email | varchar | 任意 |
| line_display_name | varchar | LINE表示名 |
| area | varchar | エリア |
| occupation | varchar | 職業 |
| favorite_drink | varchar | 好み |
| favorite_song | varchar | 好きな曲 |
| ng_topics | text | NG事項 |
| notes_summary | text | 接客要約 |
| rank_code | varchar | S/A/B/C |
| dormant_status | varchar | active/warn/dormant/long_dormant |
| last_visit_at | timestamptz | 最終来店 |
| total_visit_count | integer | 集計値 |
| total_sales_amount | numeric(12,0) | 集計値 |
| is_line_opt_in | boolean | 配信許諾 |
| is_active | boolean | 論理削除含む |
| created_at | timestamptz | 作成日時 |
| updated_at | timestamptz | 更新日時 |

#### visits

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| store_id | uuid | FK |
| customer_id | uuid | FK |
| visited_at | timestamptz | 来店日時 |
| event_name | varchar | イベント名 |
| is_accompanied | boolean | 同伴有無 |
| companion_name | varchar | 同伴者 |
| seat_minutes | integer | 滞在時間 |
| subtotal_amount | numeric(12,0) | 会計小計 |
| bottle_amount | numeric(12,0) | ボトル金額 |
| total_amount | numeric(12,0) | 合計 |
| memo_service | text | 接客メモ |
| memo_followup | text | 次回誘導メモ |
| next_followup_date | date | 推奨フォロー日 |
| created_by | uuid | 登録者 |
| created_at | timestamptz | 作成日時 |

#### campaigns

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| store_id | uuid | FK |
| name | varchar | 配信名 |
| campaign_type | varchar | broadcast/segment/individual |
| delivery_channel | varchar | line |
| status | varchar | draft/scheduled/sent/cancelled |
| scheduled_at | timestamptz | 予約日時 |
| template_id | uuid | FK |
| target_count | integer | 対象件数 |
| created_by | uuid | 作成者 |
| approved_by | uuid | 承認者 |
| created_at | timestamptz | 作成日時 |

#### message_deliveries

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| campaign_id | uuid | FK |
| customer_id | uuid | FK |
| line_user_id | varchar | LINE識別子 |
| delivery_status | varchar | queued/sent/failed |
| delivered_at | timestamptz | 配信日時 |
| error_code | varchar | エラー |
| payload_snapshot | jsonb | 配信本文スナップショット |

#### customer_notes

| カラム | 型 | 備考 |
| --- | --- | --- |
| id | uuid | PK |
| tenant_id | uuid | FK |
| customer_id | uuid | FK |
| note_type | varchar | service/followup/private_warning |
| body | text | 本文 |
| visibility | varchar | owner_only/shared |
| created_by | uuid | 作成者 |
| created_at | timestamptz | 作成日時 |

## 16. テーブル間リレーション

- 1 tenant は複数 store を持つ
- 1 store は複数 customer を持つ
- 1 customer は複数 visit を持つ
- 1 visit は複数 visit_staff を持つ
- 1 customer は複数 note を持つ
- 1 campaign は複数 message_delivery を持つ
- 1 customer は複数 tag を持つ

## 17. API設計

### 17.1 顧客

- `GET /api/customers`
- `POST /api/customers`
- `GET /api/customers/:id`
- `PATCH /api/customers/:id`
- `POST /api/customers/:id/tags`
- `POST /api/customers/:id/notes`

### 17.2 来店

- `GET /api/visits`
- `POST /api/visits`
- `GET /api/visits/:id`
- `PATCH /api/visits/:id`

### 17.3 LINE配信

- `GET /api/campaigns`
- `POST /api/campaigns`
- `POST /api/campaigns/:id/preview`
- `POST /api/campaigns/:id/approve`
- `POST /api/campaigns/:id/send`
- `GET /api/campaigns/:id/results`

### 17.4 マスタ / 設定

- `GET /api/settings/store`
- `PATCH /api/settings/store`
- `GET /api/users`
- `POST /api/users`

## 18. LINE連携設計

### 18.1 利用想定

- LINE公式アカウントを店舗ごとに保有
- システムからMessaging API経由で配信
- 顧客とLINE友だち状態を紐づける

### 18.2 連携方式

- 管理画面でLINEチャネル情報を設定
- 顧客にLINE連携用URLまたはQRを提示
- LIFFまたは識別トークン経由で顧客とLINE user IDを紐づける
- 配信対象抽出後に非同期ジョブでメッセージ送信

### 18.3 保持データ

- LINE user ID
- 友だち状態
- ブロック状態推定
- 最終配信日時
- 最終反応日時

### 18.4 制約と注意

- 個別チャット内容の全量同期は標準では対象外にする
- ブロック判定は配信失敗やイベントから補助的に扱う
- LINE公式アカウントの配信通数制限を考慮する
- オプトイン取得方針を店舗運用に組み込む

## 19. システムアーキテクチャ

### 19.1 推奨構成

- フロントエンド: Next.js App Router
- バックエンド: Next.js API または NestJS
- DB: PostgreSQL
- ORM: Prisma
- 認証: Auth.js または Clerk
- バッチ / ジョブ: cron + queue worker
- ストレージ: S3互換
- 監視: Sentry + Uptime監視

### 19.2 構成イメージ

1. ユーザーがWeb画面へアクセス
2. 認証後にAPI経由で顧客情報を取得
3. 来店登録や配信作成をDBへ保存
4. 配信ジョブがキューへ積まれる
5. WorkerがLINE Messaging APIへ送信
6. 配信結果をmessage_deliveriesへ反映

### 19.3 マルチテナント方針

- すべての主要テーブルに tenant_id を持たせる
- アプリ層で tenant_id を必須フィルタにする
- 将来の分離強化に備えてRLS導入を検討する

## 20. バックグラウンドジョブ設計

### 20.1 対象ジョブ

- LINE配信送信
- 休眠顧客再計算
- 顧客集計更新
- ボトル期限通知
- 日次レポート生成

### 20.2 実行ルール

- 一斉配信はキュー投入後に逐次送信
- API再試行を最大3回まで実施
- 失敗は運用画面で再送対象にする

## 21. 分析 / 集計設計

### 21.1 顧客KPI

- 来店回数
- 累計売上
- 平均客単価
- 最終来店日
- 直近90日来店回数
- 配信後来店有無

### 21.2 店舗KPI

- 日別売上
- 月別来店者数
- 新規 / 既存比率
- キャスト別担当売上
- イベント別来店者数

### 21.3 配信KPI

- 配信総数
- 成功数 / 失敗数
- セグメント別送信数
- 来店転換数

## 22. セキュリティ設計

### 22.1 アクセス制御

- JWTまたはセッションで認証
- ロール別認可
- tenant_idスコープの強制

### 22.2 個人情報保護

- 電話番号、メールアドレスの暗号化または秘匿化
- 管理者以外は一部マスキング表示
- 退会顧客の保管ポリシーを定義

### 22.3 監査

- ログイン履歴
- 顧客編集履歴
- 配信実行履歴
- エクスポート履歴

## 23. 運用設計

### 23.1 初期導入

- 店舗情報登録
- ユーザー発行
- 顧客CSV投入
- LINE公式アカウント接続
- テンプレート初期登録

### 23.2 日常運用

- 来店後に履歴入力
- 翌日フォロー対象確認
- 週次で休眠顧客確認
- 月次で売上と配信効果確認

### 23.3 管理ルール

- キャスト私物端末利用時は画面ロックを必須化
- 退職者アカウントは即日停止
- CSV出力は管理者のみに限定

## 24. 開発フェーズ

### Phase 1: MVP

- 認証
- 顧客管理
- 来店履歴
- 基本ダッシュボード
- LINEセグメント配信

### Phase 2: 実運用強化

- テンプレート
- 承認フロー
- 休眠自動判定
- ボトル管理
- 集計強化

### Phase 3: 拡張

- 多店舗化
- webhook連携
- 予約導線
- AI補助

## 25. 開発スケジュール案

| 期間 | 内容 |
| --- | --- |
| 1週目 | ヒアリング、要件確定、画面一覧確定 |
| 2週目 | UI設計、ER設計、LINE接続設計 |
| 3から5週目 | 顧客管理、来店履歴、認証実装 |
| 6から7週目 | 配信機能、テンプレート、分析実装 |
| 8週目 | テスト、マニュアル、導入支援 |

## 26. 見積もり分解例

### 要件定義

- 業務ヒアリング
- 画面要件整理
- データ項目整理

### 設計

- UI設計
- DB設計
- API設計
- 権限設計

### 実装

- フロント
- バックエンド
- LINE連携
- バッチ

### テスト

- 単体テスト
- 結合テスト
- 受入支援

### 導入

- 初期データ投入
- 管理者教育
- 運用マニュアル

## 27. 受注前ヒアリング項目

- 現在の顧客管理方法は紙、Excel、LINE、口頭のどれか
- 顧客数と月間来店数はどの程度か
- 使う人は何名か
- LINE公式アカウントは既にあるか
- 配信承認を誰が持つか
- 個別連絡と一斉配信をどう分けたいか
- ボトルキープ管理は必要か
- 会計システム連携は必要か
- キャスト別の閲覧制御は必要か

## 28. 受注時の提案メッセージ

このツールは単なる顧客台帳ではなく、「来店した顧客に、誰が、いつ、どのように再来店アプローチするか」を回すための運用基盤である。スナック業態で重要な関係性情報を店舗資産として蓄積し、売上再現性を上げることが狙いである。

## 29. リスクと先回り対応

### リスク

- 顧客情報入力が現場で定着しない
- LINE運用ルールが曖昧で配信品質が落ちる
- キャスト権限が広すぎて情報漏えいリスクが出る

### 対応

- 入力項目をMVPでは最小化する
- テンプレート運用を先に固める
- キャスト権限は担当顧客中心に限定する

## 30. MVP受入基準

- 顧客の登録、編集、検索ができる
- 顧客ごとに来店履歴を登録、参照できる
- セグメント条件でLINE配信対象を抽出できる
- 配信実行履歴と送信結果を確認できる
- ダッシュボードで休眠顧客を確認できる
- 権限ごとに表示制御される

