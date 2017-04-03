package ram.edu.twitterStorm.util;

public class ValueObject implements Comparable<ValueObject> {

	String key;

	Integer count;

	public ValueObject(String key, Integer count) {
		this.key = key;
		this.count = count;
	}

	public int compareTo(ValueObject valueObject) {
		return this.count.compareTo(valueObject.count);
	}

	public String getKey() {
		return key;
	}

	public void setKey(String key) {
		this.key = key;
	}

	public Integer getCount() {
		return count;
	}

	public void setCount(Integer count) {
		this.count = count;
	}

	@Override
	public boolean equals(Object valueObject) {
		return ((ValueObject) valueObject).key.equals(this.key);
	}

}
