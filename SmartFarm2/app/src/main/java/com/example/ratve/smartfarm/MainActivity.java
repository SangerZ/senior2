package com.example.ratve.smartfarm;

import android.app.ProgressDialog;
import android.app.VoiceInteractor;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private RecyclerView.Adapter adapter;
    private List<Farm> farmList;

    public String key = "5735451";
    FirebaseDatabase mydatabase = FirebaseDatabase.getInstance();
    DatabaseReference ref = FirebaseDatabase.getInstance().getReference(key);
    //    TextView TextViewTitle = (TextView) findViewById(R.id.textViewTitle);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));



        ValueEventListener postListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                String name = (String) dataSnapshot.child("Name").getValue();
                boolean HighECAlert = (boolean) dataSnapshot.child("highECAlert").getValue();
                boolean lowpHAlert = (boolean) dataSnapshot.child("lowpHAlert").getValue();

                try {
                    Farm farm = new Farm(key,name,HighECAlert,lowpHAlert);
                    farmList = Collections.singletonList(farm);
                    Log.d("test112",farm.getKey());
                    adapter = new FarmAdapter(getApplicationContext(), farmList);
                    recyclerView.setAdapter(adapter);
                }catch (Exception e){
                    e.getMessage();
                }

            }


            @Override
            public void onCancelled(DatabaseError databaseError) {

            }


//                String elevation = (String) dataSnapshot.child("ec").getValue();
//                String feel = (String) dataSnapshot.child("ph").getValue();
//                String uid = (String) dataSnapshot.child("time").getValue();


        };
        ref.addValueEventListener(postListener);

    }



}
