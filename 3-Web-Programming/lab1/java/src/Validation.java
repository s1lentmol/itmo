public class Validation {
    public boolean isValid(int x, float y, int r) {

        boolean isXValid = (x == -4 || x == -3 || x == -2 || x == -1 || x == 0 || x == 1 || x == 2 || x == 3 || x == 4);
        boolean isYValid = (y > -3 && y < 3);
        boolean isRValid = (r == 1 || r == 2 || r == 3 || r == 4 || r == 5);

        return isXValid && isYValid && isRValid;
    }
}