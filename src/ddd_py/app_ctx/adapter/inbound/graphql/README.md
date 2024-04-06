# 方針
adapter/outbound/ の GraphQL は usecase 層の手続きを呼び出すアダプターの一種。基本的に、resolver には usecase の呼び出し処理と DTO の変換処理のみを記述する。リソースに対するアクセス可否などの認可処理は usecase 側に実装されるため、ここに実装する必要はない。


また、リソースに対する基本的な Query のスキーマ定義方針は下記の通り。
- リソースへの直接的なアクセスのためのクエリには、命名に名詞のみを用いる。
- リソースに対しての特殊な操作（特殊なビューの取得・更新・削除 など）のためのクエリには、動詞から始まる命名を行う。
- フィルタリングとソーティングを伴うリソースの一括取得に用いるオブションとして、`filteringOption`,`sortingOption` を定義する。これらは find 等の検索用クエリのパラメータとして指定するために用いる。
  - filteringOptions：
    - 複数の条件を順不同の AND で指定するためのオブジェクト。
  - sortingOption：
    - 複数の条件をソート適用順に指定するためのオブジェクト。配列形式で指定する。

```graphql
directive @oneOf on INPUT_OBJECT
scalar Datetime

type Query {
    user(id: ID!): User
    users(ids: [ID!]!): [User]!

    post(id: ID!): Post
    posts(ids: [ID!]): [Post]!

    findUser(
        filteringOptions: UserFilteringOptions,
        sortingOptions: [UserSortingOption!],
        page: Page
    ): [User!]!
    findPost(
        filteringOptions: PostFilteringOptions,
        sortingOptions: [PostSortingOption!],
        page: Page
    ): [Post!]!

    getLatestPostByUser(userIds: [ID!]!): [Post]!
}

type User {
    id: ID!
    name: String!
    posts(
        filteringOptions: PostFilteringOptions,
        sortingOptions: [PostSortingOption!],
    ): [Post!]!
}

type Post {
    id: ID!
    title: String!
    content: String!
    totalViewed: Integer!
    author: User!
}

input Page {
    offset: Int!
    limit: Int!
}

input UserFilteringOptions {
    namePartial: String
    hasMinPosts: Int
}

input PostFilteringOptions {
    titlePartial: String
    contentPartial: String
    postDateFromIncl: Datetime
    postDateToExcl: Datetime
}

input UserSortingOption @oneOf {
    nameAsc: Boolean
    postsCountAsc: Boolean
}

input PostSortingOption @oneOf {
    titleAsc: Boolean
    authorNameAsc: Boolean
    viewCountSince: PostSortingOptionViewCountSince
}

input PostSortingOptionViewCountSince {
    asc: Boolean!
    viewDateFromIncl: Datetime!
}
```