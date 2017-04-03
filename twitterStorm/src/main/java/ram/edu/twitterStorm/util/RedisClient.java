package ram.edu.twitterStorm.util;

import java.util.Set;

import redis.clients.jedis.Jedis;

public class RedisClient {

	static Jedis jedis = null;
	static String collection="hashtag";
	static {
		jedis = new Jedis("localhost",6379);
	}

	public static void put(String key, Double value) {
		jedis.zadd(collection, value, key);
	}

	public static Double get(String key) {
		return jedis.zscore(collection, key);
	}
	
	public static Set<String> rank(){
		Set<String>tags=jedis.zrevrangeByScore(collection,Integer.MAX_VALUE,0,0,10);
		return tags;
	}
}
