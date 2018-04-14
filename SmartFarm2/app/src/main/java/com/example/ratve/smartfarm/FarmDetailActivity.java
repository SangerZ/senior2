package com.example.ratve.smartfarm;

import java.util.Calendar;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.widget.TextView;

import com.google.firebase.database.ChildEventListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class FarmDetailActivity extends AppCompatActivity {

    private DatabaseReference mDatabase;
    LineGraphSeries<DataPoint> seriesec;
    LineGraphSeries<DataPoint> seriesph;
    FirebaseDatabase mydatabase = FirebaseDatabase.getInstance();
//    Intent intent = getIntent();
    DatabaseReference ref = FirebaseDatabase.getInstance().getReference();

    final List<EcPhclass> ecPhlist = new ArrayList<EcPhclass>();
    String test = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //mDatabase = FirebaseDatabase.getInstance().getReference().child("5735451Data/value");

        setContentView(R.layout.activity_farm_detail);
        Intent intent = getIntent();
        String message = intent.getExtras().getString("FarmName");

        mDatabase = FirebaseDatabase.getInstance().getReference().child(message + "Data");

        ref = FirebaseDatabase.getInstance().getReference().child("value");



        final int count = 0;
//        final TextView textView = findViewByIdd(R.id.textView);
//        textView.setText(String.valueOf(ref));
//        ChildEventListener childEventListener = new ChildEventListener() {
//            @Override
//            public void onChildAdded(DataSnapshot dataSnapshot, String previousChildName) {
////                // A new data item has been added, add it to the list
//                EcPhclass message = dataSnapshot.getValue(EcPhclass.class);
//                ecPhlist.add(message);
//            }
//
//            @Override
//            public void onChildChanged(DataSnapshot dataSnapshot, String previousChildName) {
//
//                test = String.valueOf(dataSnapshot.getValue());
//
//            }
//
//
//            @Override
//            public void onChildRemoved(DataSnapshot dataSnapshot) {
//                // A data item has been removed
//                EcPhclass message = dataSnapshot.getValue(EcPhclass.class);
//            }
//
//            @Override
//            public void onChildMoved(DataSnapshot dataSnapshot, String previousChildName) {
////                Log.d("test", "onChildMoved:" + dataSnapshot.getKey());
////
////                // A data item has changed position
////                Comment movedComment = dataSnapshot.getValue(Comment.class);
////                Message message = dataSnapshot.getValue(Message.class);
//            }
//
//            @Override
//            public void onCancelled(DatabaseError databaseError) {
////                Log.w(TAG, "onCancelled", databaseError.toException());
////                Toast.makeText(mContext, "Failed to load data.", Toast.LENGTH_SHORT).show();
//            }
//        };
//        ValueEventListener valueEventListener = new ValueEventListener() {
//            @Override
//            public void onDataChange(DataSnapshot dataSnapshot) {
//
//                test =(String) dataSnapshot.child("-LA1Q1hIMaWHg1WxF-HW\\n").getValue();
//                Log.d("1221",test);
//            }
//
//            @Override
//            public void onCancelled(DatabaseError databaseError) {
//
//            }
//        };

//        ref.addValueEventListener(valueEventListener);
//        ref.addValueEventListenerdChildEventListener(childEventListener);
//        textView.setText(String.valueOf(mydatabase.getReference().child("value").getKey().toString()));
//            ChildEventListener childEventListener = new ChildEventListener() {
//
//                @Override
//                public void onChildAdded(DataSnapshot dataSnapshot, String s) {
//                    Log.d("test", "onChildChanged:" + dataSnapshot.getKey());
////
//                // A data item has changed
//                    EcPhclass message2 = dataSnapshot.getValue(EcPhclass.class);
//                    textView.setText(String.valueOf(message2));
////                    if(true){
////                        EcPhlist = Collections.singletonList(message2);
////                    }
////
////                    try {
////                        Log.d("test112", String.valueOf(message));
////
////                    }catch (Exception e){
////                        e.getMessage();
////                    }
//
//                }
//
//                @Override
//                public void onChildChanged(DataSnapshot dataSnapshot, String s) {
//
//                }
//
//                @Override
//                public void onChildRemoved(DataSnapshot dataSnapshot) {
//
//                }
//
//                @Override
//                public void onChildMoved(DataSnapshot dataSnapshot, String s) {
//
//                }
//
//                @Override
//                public void onCancelled(DatabaseError databaseError) {
//
//                }
//            };
////            textView.setText(String.valueOf(EcPhlist));

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        MenuInflater inflater = getMenuInflater();
        //inflater.inflate(R);
        return true;
    }

    @Override
    protected void onStart() {
        super.onStart();


        final GraphView graphView = (GraphView) findViewById(R.id.graph);
        seriesec = new LineGraphSeries<DataPoint>();

        mDatabase.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(DataSnapshot dataSnapshot, String s) {
//                String str = dataSnapshot.getKey();
//                String str2 = (String) dataSnapshot.child(dataSnapshot.getKey()).getValue();

//                for (DataSnapshot childDataSnapshot : dataSnapshot.getChildren()) {
//                    Log.v(TAG,""+ childDataSnapshot.getKey()); //displays the key for the node
//                    Log.v(TAG,""+ childDataSnapshot.child("ec").getValue());   //gives the value for given keyname
//                }
//

                int count = 0;
                Date currentTime = Calendar.getInstance().getTime();
                String curtime = String.valueOf(currentTime).substring(0,10);
                for(DataSnapshot childDataSnapshot : dataSnapshot.getChildren()) {
                    EcPhclass ecPhclass = childDataSnapshot.getValue(EcPhclass.class);
                    Log.d("test1335", ecPhclass.time.substring(0, 10));
                    String strtime = ecPhclass.time.substring(0, 10);
                    if (strtime.equals(curtime)) {
                        ecPhlist.add(ecPhclass);

                    }
                }
                DataPoint[] dataPoint = new DataPoint[ecPhlist.size()];
                for(int i = 0 ; i < ecPhlist.size(); i++) {
                    EcPhclass a = ecPhlist.get(i);
                    double x = a.getEc();
                    double y = Double.parseDouble((a.getTime().substring(11, 20).replace(":", "")));
                    y = y / 10000;
                    //dataPoint[i] = new DataPoint(x,y);
                    dataPoint[i] = new DataPoint(y,x);
                }
                    //seriesec.appendData(new DataPoint(x, Double.parseDouble(y)),true,500);
//                    seriesec.appendData(new DataPoint(x, y) ,true,ecPhlist.size());


                seriesec = new LineGraphSeries<DataPoint>(dataPoint);
                graphView.addSeries(seriesec);

            }


            @Override
            public void onChildChanged(DataSnapshot dataSnapshot, String s) {

            }

            @Override
            public void onChildRemoved(DataSnapshot dataSnapshot) {

            }

            @Override
            public void onChildMoved(DataSnapshot dataSnapshot, String s) {

            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });

    }

}
