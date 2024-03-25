DELETE from user
where
    left(google_sub, 1) = "t";