SOCIAL_INTELLIGENCE_READ_DB_SECRET_ID = "social-intelligence-read-db"
SOCIAL_INTELLIGENCE_DB_SECRET_ID = "social-intelligence-db"

GET_TOKEN_DETAILS_FROM_SYMBOL_QUERY = """
WITH tokens AS (
    SELECT "eth" AS chain, p.token_id, p.latest_liquidity_usd, p.latest_market_cap, 
    (pop.buy_vol_24_hr_usd + pop.sell_vol_24_hr_usd) AS vol_24_hr, token_symbol
    FROM social.pairs AS p
    LEFT JOIN social.pairs_onchain_properties AS pop
    ON p.pair_id = pop.pair_id
    WHERE p.token_symbol = %(symbol)s
    HAVING vol_24_hr > 0
    UNION ALL
    SELECT chain, address AS token_id, liquidity, marketcap, vol24hUSD AS vol_24_hr,
    symbol AS token_symbol
    FROM blockchains.tokens 
    WHERE symbol = %(symbol)s
    HAVING vol_24_hr > 0
)
SELECT * 
FROM tokens
ORDER BY vol_24_hr DESC
LIMIT %(limit)s
"""

GET_TOKEN_SYMBOL_FOR_MULTIPLE_SYMBOLS_QUERY = """
WITH tokens AS (
    SELECT "eth" AS chain, p.token_id, p.latest_liquidity_usd, p.latest_market_cap, 
    (pop.buy_vol_24_hr_usd + pop.sell_vol_24_hr_usd) AS vol_24_hr, p.token_symbol
    FROM social.pairs AS p
    LEFT JOIN social.pairs_onchain_properties AS pop
    ON p.pair_id = pop.pair_id
    WHERE p.token_symbol IN {symbols}
    HAVING vol_24_hr > 0
    UNION ALL
    SELECT chain, address AS token_id, liquidity, marketcap, vol24hUSD AS vol_24_hr, symbol AS token_symbol
    FROM blockchains.tokens 
    WHERE symbol IN {symbols}
    HAVING vol_24_hr > 0
)
SELECT * 
FROM (
    SELECT *,
    DENSE_RANK() OVER (PARTITION BY token_symbol ORDER BY vol_24_hr DESC) AS token_rank
    FROM tokens
    ORDER BY vol_24_hr DESC
) AS sub
WHERE token_rank <= %(limit)s
"""

GET_ACTIVE_COINS_DATA_QUERY = """
SELECT symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, 
marketcap, icon, buy_tax, sell_tax, pair_created_at, twitter, telegram, website
FROM blockchains.active_symbols
WHERE marketcap >= 50000000
AND is_coin 
AND ({search_condition})
ORDER BY marketcap DESC
"""

GET_ACTIVE_SYMBOLS_DATA_QUERY = """
WITH ranked_token AS (
    SELECT 
        overall_rank, token_rank, pair_rank, symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, 
        marketcap, icon, buy_tax, sell_tax, pair_created_at, twitter, telegram, website,
        ((liquidity * 7) + (marketcap * 2) + (vol_24_hr * 7)) AS score,
        ROW_NUMBER() OVER (PARTITION BY chain_id ORDER BY ((liquidity * 7) + (marketcap * 2) + (vol_24_hr * 7)) DESC) AS row_num
    FROM blockchains.active_symbols
    WHERE NOT is_coin 
    AND ({search_condition})
    AND vol_24_hr >= 500 
    AND liquidity >= 5000
    AND marketcap >= 20000
), all_chains_top_result AS (
	SELECT 
    	overall_rank, token_rank, pair_rank, symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, 
		marketcap, icon, buy_tax, sell_tax, pair_created_at, twitter, telegram, website, score, 1 AS order_number
	FROM ranked_token
	WHERE row_num = 1
	ORDER BY score DESC
	LIMIT {internal_search_limit}
), remaining_Results AS (
	SELECT 
		overall_rank, token_rank, pair_rank, symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, 
	    marketcap, icon, buy_tax, sell_tax, pair_created_at, twitter, telegram, website, score, 2 AS order_number
	FROM ranked_token
	WHERE token_id NOT IN (SELECT token_id FROM all_chains_top_result)
	AND pair_rank = 1
	ORDER BY score DESC
)	
SELECT symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, marketcap, icon, 
buy_tax, sell_tax, pair_created_at, twitter, telegram, website, order_number, score
FROM all_chains_top_result
UNION
SELECT symbol, name, is_coin, chain_id, token_id, pair_id, vol_24_hr, liquidity, marketcap, icon, 
buy_tax, sell_tax, pair_created_at, twitter, telegram, website, order_number, score
FROM remaining_Results
ORDER BY order_number, score DESC
LIMIT {limit}
OFFSET {start}
"""

GET_AUTHOR_HANDLE_DETAILS_FROM_TWITTER_PROFILE_QUERY = """
(
    SELECT name, handle, profile_image_url, followers_count, followings_count
    FROM tickr.twitter_profile
    WHERE handle LIKE '{author_handle}%'
    ORDER BY followers_count DESC
    LIMIT {limit}
)
UNION ALL
(
    SELECT name, handle, profile_image_url, followers_count, followings_count
    FROM tickr.twitter_profile
    WHERE name LIKE '{author_handle}%'
    AND NOT EXISTS (
        SELECT 1
        FROM tickr.twitter_profile
        WHERE handle LIKE '{author_handle}%'
    )
    ORDER BY followers_count DESC
    LIMIT {limit}
)
LIMIT {limit}
OFFSET {start};
"""

GET_AUTHOR_HANDLE_DETAILS_FROM_TWITTER_PROFILE_EXACT_MATCH_QUERY = """
SELECT name, handle, profile_image_url, followers_count, followings_count
FROM tickr.twitter_profile
WHERE handle = '{author_handle}'
OR name = '{author_handle}'
ORDER BY followers_count DESC
LIMIT {limit}
OFFSET {start};
"""

SEARCH_TELEGRAM_DATA_QUERY = """
SELECT
    tcp.channel_id,
    tcp.total_mentions,
    tcp.token_mentions,
    tcp.average_mentions_per_day,
    te.name,
    te.image_url,
    te.tg_link,
    te.members_count,
    te.channel_age,
    tcp.win_rate_30_day
FROM
    telegram.telegram_channel_properties AS tcp
LEFT JOIN
    telegram.telegram_entity AS te
ON
    tcp.channel_id = te.channel_id
WHERE
    te.name LIKE '%{search_term}%'
    ORDER BY tcp.total_mentions DESC
LIMIT {limit}
OFFSET {start};
"""

SEARCH_TELEGRAM_DATA_EXACT_MATCH_QUERY = """
SELECT
    tcp.channel_id,
    tcp.total_mentions,
    tcp.token_mentions,
    tcp.average_mentions_per_day,
    te.name,
    te.image_url,
    te.tg_link,
    te.members_count,
    te.channel_age,
    tcp.win_rate_30_day
FROM
    telegram.telegram_channel_properties AS tcp
LEFT JOIN
    telegram.telegram_entity AS te
ON
    tcp.channel_id = te.channel_id
WHERE
    te.name = '{search_term}'
    ORDER BY tcp.total_mentions DESC
LIMIT {limit}
OFFSET {start};
"""

GET_TWEETS_QUERY = """
SELECT tweet_id, body, author_handle, tweet_create_time
FROM twitter.enhanced_tweets
WHERE {where_condition}
ORDER BY tweet_create_time DESC
LIMIT {limit}
OFFSET {start};
"""

GET_CONFIGURATION_FOR_SEARCH_QUERY = """
SELECT search
FROM blockchains.configuration
"""
