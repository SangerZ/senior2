package com.example.ratve.smartfarm;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.app.VoiceInteractor;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.renderscript.ScriptGroup;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.InputType;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.Toast;

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

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private RecyclerView.Adapter adapter;
    private List<Farm> farmList = new ArrayList<Farm>();

    public String[] key = {"5735451","5812345"};
    List<String> fileFarmList;// = new ArrayList<String>();
    FirebaseDatabase mydatabase = FirebaseDatabase.getInstance();
    DatabaseReference ref = FirebaseDatabase.getInstance().getReference();

    Farm farm;
    EditText userInput;
    private static final String fileName = "file.txt";

    File file;// = new File(fileName);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        File fileDir = this.getFilesDir();
        file = new File(fileDir, fileName);
        if(!file.exists()){
            file = new File(this.getFilesDir(), fileName);
        }
        else{
            readFile(fileName);
        }

        recyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        ValueEventListener postListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                try{
                    String name = (String) dataSnapshot.child("name").getValue();
                    boolean HighECAlert = (boolean) dataSnapshot.child("highECAlert").getValue();
                    boolean lowpHAlert = (boolean) dataSnapshot.child("lowpHAlert").getValue();
                    farm = new Farm(dataSnapshot.getKey(),name,HighECAlert,lowpHAlert);
                    farmList.add(farm);


                    adapter = new FarmAdapter(getApplicationContext(), farmList);
                    recyclerView.setAdapter(adapter);

                }catch (Exception e){
                    e.getMessage();
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        };

        if(fileFarmList != null) {
            for (int i = 0; i < fileFarmList.size(); i++) {
                ref = FirebaseDatabase.getInstance().getReference(fileFarmList.get(i));
                ref.addValueEventListener(postListener);
            }
        }

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        final AlertDialog alertDialog;
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("New Farm Insertion");
        builder.setMessage("Please type the farm number that you want to add");

        userInput = new EditText(this);
        userInput.setInputType(InputType.TYPE_CLASS_NUMBER);
        builder.setView(userInput);
        builder.setPositiveButton("Submit", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String txt = userInput.getText().toString();
                //Toast.makeText(getApplicationContext(), txt, Toast.LENGTH_SHORT).show();
                Boolean check = false;
                if(fileFarmList != null){
                    for (int i = 0; i < fileFarmList.size(); i++) {
                        if(txt.equals(fileFarmList.get(i))){
                            check = true;
                            break;
                        }
                    }

                }
                if (check){
                    Toast.makeText(getApplicationContext(), txt + " is exist ", Toast.LENGTH_SHORT).show();
                }else {

                    saveFile(fileName, txt);
                }


                Intent intent = getIntent();
                finish();
                startActivity(intent);
            }
        });
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
        alertDialog = builder.create();
        switch(item.getItemId()){

            case R.id.add_new:
                alertDialog.show();
                return true;
        }
        return super.onOptionsItemSelected(item);
    }


    public void saveFile(String file, String text){
        String submitting = "\r\n" + text;
        try{
            FileOutputStream fos = openFileOutput(file, Context.MODE_APPEND);
            //FileOutputStream fos = openFileOutput(file, );
            fos.write(submitting.getBytes());
            //fos.write
            fos.close();
            Toast.makeText(MainActivity.this, "Save success", Toast.LENGTH_SHORT).show();
        }catch (Exception e){
            e.printStackTrace();
            Toast.makeText(MainActivity.this, "Error saving file", Toast.LENGTH_SHORT).show();
        }
    }

    public void readFile(String file){

        String text = "";
        try{
            FileInputStream fis = openFileInput(file);
            int size = fis.available();
            byte[] buffer = new byte[size];
            fis.read(buffer);
            fis.close();
            text = new String(buffer);
            fileFarmList = new ArrayList<String>(Arrays.asList(text.split("\r\n")));
            //Toast.makeText(MainActivity.this, fileFarmList.get(0), Toast.LENGTH_LONG).show();

        }catch (Exception e){
            Toast.makeText(MainActivity.this, "Error reading file", Toast.LENGTH_SHORT).show();
        }
    }
}
