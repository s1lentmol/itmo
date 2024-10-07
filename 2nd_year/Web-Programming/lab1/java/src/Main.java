import com.fastcgi.FCGIInterface;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedHashMap;

public class Main {
    public static void main(String[] args){
        FCGIInterface fcgiInterface = new FCGIInterface();
        CheckInArea check = new CheckInArea();
        Validation validation = new Validation();
        while (fcgiInterface.FCGIaccept() >= 0) {
            String method = FCGIInterface.request.params.getProperty("REQUEST_METHOD");
            if (method.equals("GET")) {
                long startTime = System.nanoTime();
                String queryString = FCGIInterface.request.params.getProperty("QUERY_STRING");
                if (queryString!=null) {
                    HashMap<String, String> values = getValues(queryString);
                    boolean isHit;
                    boolean isValid;
                    try{
                        isValid = validation.isValid(Integer.parseInt(values.get("x")), Float.parseFloat(values.get("y")), Integer.parseInt(values.get("r")));
                        isHit = check.checkHit(Integer.parseInt(values.get("x")), Float.parseFloat(values.get("y")), Integer.parseInt(values.get("r")));
                    } catch (Exception e){
                        System.out.println(error("not valid data"));
                        continue;
                    }
                    if (isValid){
                        System.out.println(response(isHit,values.get("x"),values.get("y"),values.get("r"), startTime));
                    } else{
                        System.out.println(error("not valid data"));
                    }
                } else {
                    System.out.println(error("empty"));
                }
            }
            else{x
                System.out.println(error("wrong method"));
            }
        }
    }
    private static LinkedHashMap<String, String> getValues(String inpString){
        String[] args = inpString.split("&");
        LinkedHashMap<String, String> values = new LinkedHashMap<>();
        for (String s : args) {
            String[] arg = s.split("=");
            values.put(arg[0], arg[1]);
        }
        return values;
    }

    private static String response(boolean isHit, String x, String y, String r, long startTime) {
        long endTime = System.nanoTime();
        long duration = (endTime - startTime);
        String scrTime = duration + " нс"; // в наносекундах

        SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yy HH:mm:ss");
        String currentDateTime = sdf.format(new Date());
        String content = """
                {"result":"%s","x":"%s","y":"%s","r":"%s","currTime":"%s","scrTime":"%s","error":"not"}
                """.formatted(isHit, x, y, r,currentDateTime,scrTime);
        return """
                Content-Type: application/json
                Content-Length: %d
                
                %s
                """.formatted(content.getBytes(StandardCharsets.UTF_8).length, content);
    }

    private static String error(String msg) {
        String content = """
                {"error":"%s"}
                """.formatted(msg);
        return """
                Content-Type: application/json
                Content-Length: %d
                
                %s
                """.formatted(content.getBytes(StandardCharsets.UTF_8).length, content);
    }
}


