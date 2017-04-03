package ram.edu.twitterStorm.util;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

public class Util {

	public static long getDiff(long start) {
		return Calendar.getInstance().getTimeInMillis() - start;
	}

	public static long reset() {
		return Calendar.getInstance().getTimeInMillis();
	}
	
	public static TreeMap<Integer, List<String>> sortMap(Map<String,Integer> inputMap){
		TreeMap<Integer,List<String>> rankMap = new TreeMap<Integer,List<String>>();
		for(Entry<String,Integer> entry:inputMap.entrySet()){
			List<String> keys=new ArrayList<String>();
			if(rankMap.containsKey(entry.getValue())){
				keys=rankMap.get(entry.getValue());
			}
			keys.add(entry.getKey());
			rankMap.put(entry.getValue(), keys);
		}
		return rankMap;
		
	}
}
