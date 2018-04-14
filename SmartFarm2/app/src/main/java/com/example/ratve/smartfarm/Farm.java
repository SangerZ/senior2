package com.example.ratve.smartfarm;

/**
 * Created by ratve on 19/2/2561.
 */

public class Farm {

    //private int id;
    private String name,key;
    private boolean highECAlert, lowpHAlert;


    public Farm(String key ,String name, boolean highECAlert,boolean lowpHAlert) {
        //this.id = id;
        this.key = key;
        this.name = name;
        this.highECAlert = highECAlert;
        this.lowpHAlert = lowpHAlert;
    }

    public Farm(boolean highECAlert, boolean lowpHAlert) {
    }

    public  String getKey(){ return key;}

    public String getName() {
        return name;
    }

    public boolean gethighECAlert() {
        return highECAlert;
    }

    public boolean getlowpHAlert() {
        return lowpHAlert;
    }


    public  void setKey(String key){this.key = key;}

    public void setName(String name) {
        this.name = name;
    }

    public void sethighECAlert(boolean highECAlert) {
        this.highECAlert = highECAlert;
    }

    public void setlowpHAlert(boolean lowpHAlert) {
        this.lowpHAlert = lowpHAlert;
    }
}