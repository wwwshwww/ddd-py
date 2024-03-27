# 方針
adapter/outbound/ の GraphQL は、クライアントの指定したクエリに基づき usecase 層の手続きを呼び出す。各 resolver に実装する要素は、usecase の呼び出し処理と DTO の変換処理のみがとなる想定。リソースに関する認可は usecase に実装されるため、ここで記述する必要はない。


リソースに対する基本的な Query のスキーマ定義方針は以下の通り。特殊なビュー取得の必要が生じた場合、都度クエリを追加する。

```graphql
type Query {
    user(id: ID!): User
    users(ids: [ID!]): [User]
    post(id: ID!): Post
    posts(ids: [ID!]): [Post]
    findPosts(
        filter: PostFilteringOptions, 
        sorter: [PostSortingOption], 
        page: Page
    ): [Post]
}

type User {
    id: ID!
    name: String
    posts(filter: PostFilteringOptions): [Post]
}

type Post {
    id: ID!
    title: String
    content: String
    author: User
}

input Page {
    offset: int!
    limit: int!
}

input PostFilteringOptions {
    keyword: String
    startDateIncl: String
    endDateExcl: String
}

interface PostSortingOption {
    asc: Boolean
}

input PostSortingOptionDate implements PostSortingOption {
    asc: Boolean
}

input PostSortingOptionSpecifiedReactionCount implements PostSortingOption {
    asc: Boolean
    reactionType: String
}
```