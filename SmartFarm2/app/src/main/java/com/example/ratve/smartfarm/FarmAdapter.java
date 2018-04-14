package com.example.ratve.smartfarm;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.support.v7.widget.RecyclerView;
import android.text.Layout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import java.util.List;

/**
 * Created by ratve on 19/2/2561.
 */

public class FarmAdapter extends RecyclerView.Adapter<FarmAdapter.FarmViewHolder>  {

    private Context nCtx;
    private List<Farm> farmList;


    public FarmAdapter(Context nCtx, List<Farm> farmList) {
        this.nCtx = nCtx;
        this.farmList = farmList;
    }

    @Override
    public FarmViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        //return null;
        //LayoutInflater inflater = LayoutInflater.from(nCtx);
        //View view = inflater.inflate(R.layout.main_layout, null);
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.main_layout, parent, false);

        FarmViewHolder holder = new FarmViewHolder(view);
        return holder;
    }

    @Override
    public void onBindViewHolder(FarmViewHolder holder, int position) {
        final Farm farm = farmList.get(position);
        holder.textViewName.setText(farm.getName());
        holder.textViewEC.setText(String.valueOf(farm.gethighECAlert()));
        holder.textViewPH.setText(String.valueOf(farm.getlowpHAlert()));

        //holder.imageView.setImageDrawable();
//        Picasso.with(nCtx)
//                .load(farm.getImageURL())
//                .into(holder.imageView);

        holder.relativeLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                v.setBackgroundColor(Color.parseColor("#697066"));
                //Context context = v.getContext();
                String str = farm.getKey();
                Intent intent = new Intent(nCtx, FarmDetailActivity.class);
                intent.putExtra("FarmName", str);
                nCtx.startActivity(intent);
            }
        });
    }

    @Override
    public int getItemCount() {
        //return 0;
        return farmList.size();
    }

    class FarmViewHolder extends RecyclerView.ViewHolder{

        ImageView imageView;
        TextView textViewName, textViewEC, textViewPH, textViewTemp;
        RelativeLayout relativeLayout;

        public FarmViewHolder(View itemView) {
            super(itemView);

//            imageView = itemView.findViewById(R.id.imageView);
            textViewName = itemView.findViewById(R.id.textViewTitle);
            textViewEC = itemView.findViewById(R.id.textViewEC);
            textViewPH = itemView.findViewById(R.id.textViewPH);
//            textViewTemp = itemView.findViewById(R.id.textViewTemp);
            relativeLayout = itemView.findViewById(R.id.relativeLayout);
        }
    }


}
