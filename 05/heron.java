public class heron{
    public static void main(String[] args){
        for(float i = 1.0f; i < 10.0E19f;i++){
            if(heron_area((float)i,1.0f) == 0.0){
                System.out.println(i);
                break;
            }
        }
        System.out.println("Printing 10^28 for baseht_area: " +
                           baseht_area(10.0E28f,1.0f));
        System.out.println("HERON_AREA: " + heron_area((float)10.0E19f,1.0f));
        System.out.println("BASEHT_AREA: " + baseht_area((float)10.0E19f,1.0f));
    }

    public static float heron_area(float a, float c){
        float s = (a+a+c)/2.0f;
        return (s-a)*((float)Math.sqrt(s*(s-c)));
    }

    public static float baseht_area(float a, float c){
        float d = c/(2.0f*a);
        return ((((float)Math.sqrt(1.0f-d*d)*a)*c)*0.5f);
    }
}
