package com.example.ratve.smartfarm;

import java.text.DateFormatSymbols;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.util.Calendar;

import android.annotation.TargetApi;
import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

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
    DatePickerDialog.OnDateSetListener datepicker;
    FirebaseDatabase mydatabase = FirebaseDatabase.getInstance();
//    Intent intent = getIntent();
    DatabaseReference ref = FirebaseDatabase.getInstance().getReference();

    final List<EcPhclass> ecPhlist = new ArrayList<EcPhclass>();
    String datepickerDate = "";
    Date currentTime = Calendar.getInstance().getTime();
    String curtime = String.valueOf(currentTime).substring(0,10);
    String test = "";
    String message = "";

    EditText ecInput;
    EditText phInput;
    EditText nameInput;
    EditText volumeInput;

    public String monthChange(int month){
        String answer = "";
        switch (month){
            case 1:
                answer = "Jan";
                break;
            case 2:
                answer = "Feb";
                break;
            case 3:
                answer = "Mar";
                break;
            case 4:
                answer = "Apr";
                break;
            case 5:
                answer = "May";
                break;
            case 6:
                answer = "Jun";
                break;
            case 7:
                answer = "Jul";
                break;
            case 8:
                answer = "Aug";
                break;
            case 9:
                answer = "Sep";
                break;
            case 10:
                answer = "Oct";
                break;
            case 11:
                answer = "Nov";
                break;
            case 12:
                answer = "Dec";
                break;
        }
        return answer;
    }

    public String dayOfWeekChange(int day){
        String answer = "";
        switch(day){
            case 0:
                answer = "Sat";
                break;
            case 1:
                answer = "Sun";
                break;
            case 2:
                answer = "Mon";
                break;
            case 3:
                answer = "Tue";
                break;
            case 4:
                answer = "Wed";
                break;
            case 5:
                answer = "Thu";
                break;
            case 6:
                answer = "Fri";
                break;
        }
        return answer;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_farm_detail);
        Intent intent = getIntent();
        message = intent.getExtras().getString("FarmName");
        mDatabase = FirebaseDatabase.getInstance().getReference().child(message + "Data");
        ref = FirebaseDatabase.getInstance().getReference().child("value");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        MenuInflater inflater = getMenuInflater();
        getMenuInflater().inflate(R.menu.menu, menu);
        //inflater.inflate(R);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id== R.id.setec){
            //Toast.makeText(this,"test1",Toast.LENGTH_SHORT).show();
            final AlertDialog alertDialog;
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("Configuration");
            nameInput = new EditText(this);
            volumeInput = new EditText(this);
            phInput = new EditText(this);
            ecInput = new EditText(this);

            nameInput.setText("name");
            volumeInput.setText("volume");
            phInput.setText("ph");
            ecInput.setText("ec");

            volumeInput.setInputType(InputType.TYPE_CLASS_NUMBER);
            ecInput.setInputType(InputType.TYPE_NUMBER_FLAG_DECIMAL);
            phInput.setInputType(InputType.TYPE_NUMBER_FLAG_DECIMAL);

            Context ctx = this;
            LinearLayout layout = new LinearLayout(ctx);
            layout.setOrientation(LinearLayout.VERTICAL);
            layout.addView(nameInput);
            layout.addView(volumeInput);
            layout.addView(phInput);
            layout.addView(ecInput);

            builder.setView(layout);

            builder.setPositiveButton("Submit", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    updateConfiguration(nameInput.getText().toString(),
                            Integer.parseInt(volumeInput.getText().toString()),
                            Float.parseFloat(phInput.getText().toString()),
                            Float.parseFloat(ecInput.getText().toString()));
                    dialog.dismiss();
                }
            });
            builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });
            alertDialog = builder.create();
            alertDialog.show();
        }

        if(id == R.id.date){
            Calendar calendar = Calendar.getInstance();
            int y = calendar.get(Calendar.YEAR);
            int m = calendar.get(Calendar.MONTH);
            int d = calendar.get(Calendar.DAY_OF_MONTH);
            DatePickerDialog dialog = new DatePickerDialog(
                    FarmDetailActivity.this,
                    android.R.style.Theme_Holo_Dialog_MinWidth
                    , datepicker
                    , y, m, d);
            dialog.getDatePicker().setMaxDate(new Date().getTime());
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
            dialog.show();
        }
        datepicker = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
                Date date = new Date(year, month, dayOfMonth);
                int day = date.getDay();
                month = month + 1;
                String monthStr = monthChange(month);
                String dayOfWeek = dayOfWeekChange(day);
                //datepickerDate = monthStr + "/" + dayOfMonth + "/" + year + "/" + dayOfWeek;
                datepickerDate = dayOfWeek + " " + monthStr + " " + dayOfMonth;
                Toast.makeText(FarmDetailActivity.this, datepickerDate, Toast.LENGTH_SHORT).show();
            }
        };

        return super.onOptionsItemSelected(item);
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

                currentTime = Calendar.getInstance().getTime();
                curtime = String.valueOf(currentTime).substring(0,10);
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

    private void updateConfiguration(String name, int volume, float ph, float ec){

        DatabaseReference databaseReference = FirebaseDatabase.getInstance().getReference().child(message);
        Farm farm = new Farm(name, volume, ph, ec);
        databaseReference.setValue(farm);
    }

}
