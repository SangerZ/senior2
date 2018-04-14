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


        final GraphView graphView = (GraphView) findViewById(R.id.graph_ec);
        graphView.setTitle("EC Graph");
        final GraphView graphView2 = (GraphView) findViewById(R.id.graph_ph);
        graphView2.setTitle("pH Graph");
        seriesec = new LineGraphSeries<DataPoint>();
        seriesph = new LineGraphSeries<DataPoint>();

        mDatabase.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(DataSnapshot dataSnapshot, String s) {

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
                DataPoint[] dataPointPH = new DataPoint[ecPhlist.size()];
                for(int i = 0 ; i < ecPhlist.size(); i++) {
                    EcPhclass a = ecPhlist.get(i);
                    double x = a.getEc();
                    double p = a.getPh();
                    double y = Double.parseDouble((a.getTime().substring(11, 20).replace(":", "")));
                    y = y / 10000;
                    //dataPoint[i] = new DataPoint(x,y);
                    dataPoint[i] = new DataPoint(y,x);
                    dataPointPH[i] = new DataPoint(y,p);
                }

                seriesec = new LineGraphSeries<DataPoint>(dataPoint);
                seriesph = new LineGraphSeries<DataPoint>(dataPointPH);
                graphView.addSeries(seriesec);
                graphView2.addSeries(seriesph);

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
