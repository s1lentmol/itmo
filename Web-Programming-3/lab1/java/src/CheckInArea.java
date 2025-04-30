public class CheckInArea {

    public boolean checkHit(int x, float y, int r){
        return checkInTriangle(x, y, r) || checkInRectangle(x, y, r) || checkInCircle(x, y, r);
    }

    public boolean checkInTriangle(int x, float y, int r){
        return (y <= -x + (float) r / 2) && (y >= 0) && (x <= 0);
    }

    public boolean checkInRectangle(int x, float y, int r){
        return (x<=0) && (x>= -r) && (y >= (float) -r/2) && (y<=0);
    }

    public boolean checkInCircle(int x, float y, int r){
        return (x*x+y*y <= r*r) && (y<=0) && (x>=0);
    }
}
