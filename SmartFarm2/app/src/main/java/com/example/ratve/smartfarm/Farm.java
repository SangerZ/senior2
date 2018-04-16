package com.example.ratve.smartfarm;

/**
 * Created by ratve on 19/2/2561.
 */

public class Farm {

    //private int id;
    private String name,key;
    private boolean highECAlert, lowpHAlert;
    private int volume;
    private float phTreshold, ecTreshold;


    public Farm(String key ,String name, boolean highECAlert,boolean lowpHAlert) {
        //this.id = id;
        this.key = key;
        this.name = name;
        this.highECAlert = highECAlert;
        this.lowpHAlert = lowpHAlert;
    }

    public Farm(boolean highECAlert, boolean lowpHAlert) {
    }

    public Farm(String name, int volume, float phTreshold, float ecTreshold){

        this.name = name;
        this.volume = volume;
        this.phTreshold = phTreshold;
        this.ecTreshold = ecTreshold;
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

    public int getVolume() {
        return volume;
    }

    public void setVolume(int volume) {
        this.volume = volume;
    }

    public float getPhTreshold() {
        return phTreshold;
    }

    public void setPhTreshold(float phTreshold) {
        this.phTreshold = phTreshold;
    }

    public float getEcTreshold() {
        return ecTreshold;
    }

    public void setEcTreshold(float ecTreshold) {
        this.ecTreshold = ecTreshold;
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