# 方針
adapter/outbound/ の GraphQL は、クライアントの指定したクエリに基づき usecase 層の手続きを呼び出す。各 resolver に実装する要素は、usecase の呼び出し処理と DTO の変換処理のみがとなる想定。リソースに関する認可は usecase に実装されるため、ここで記述する必要はない。


リソースに対する基本的な Query のスキーマ定義方針は以下の通り。特殊なビュー取得の必要が生じた場合、都度クエリを追加する。

```graphql
directive @oneOf on INPUT_OBJECT
scalar Datetime

type Query {
    user(id: ID!): User
    users(ids: [ID!]!): [User]!
    findUser(
        filteringOptions: UserFilteringOptions,
        sortingOptions: [UserSortingOption!],
        page: Page
    ): [User!]!

    post(id: ID!): Post
    posts(ids: [ID!]): [Post]!
    findPost(
        filteringOptions: PostFilteringOptions,
        sortingOptions: [PostSortingOption!],
        page: Page
    ): [Post!]!
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