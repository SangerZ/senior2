package com.example.ratve.smartfarm;

import com.google.firebase.database.Exclude;

import java.util.HashMap;
import java.util.Map;

class EcPhclass {
    public float ec;
    public float ph;
    public String time;

    public EcPhclass() {
        // Default constructor required for calls to DataSnapshot.getValue(Post.class)
    }

    public float getEc() {
        return ec;
    }

    public void setEc(float ec) {
        this.ec = ec;
    }

    public float getPh() {
        return ph;
    }

    public void setPh(float ph) {
        this.ph = ph;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public EcPhclass(float ec, float ph, String time) {
        this.ec = ec;
        this.ph = ph;
        this.time = time;
    }

    @Exclude
    public Map<String, Object> toMap() {
        HashMap<String, Object> result = new HashMap<>();
        result.put("ec", ec);
        result.put("ph", ph);
        result.put("time", time);

        return result;
    }

}
