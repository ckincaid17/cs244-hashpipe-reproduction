metadata tracking_metadata_t hashpipe_meta;

field_list hash_list {
    hashpipe_meta.mKeyCarried;
}

field_list_calculation stage1_hash {
    input {
        hash_list;
    }
    algorithm : hashpipe_1;
    output_width : 5;
}

field_list_calculation stage2_hash {
    input {
        hash_list;
    }
    algorithm : hashpipe_2;
    output_width : 5;
}

header_type tracking_metadata_t {
    fields {
        bit<32> mKeyInTable;
        bit<32> mCountInTable;
        bit<5> mIndex;
        bit<1> mValid;
        bit<32> mKeyCarried;
        bit<32> mCountCarried;
        bit<32> mDiff;
    }
}

register flow_tracker_stage1 {
    width: 32;
    static: track_stage1;
    instance_count: 32;
}

register packet_counter_stage1 {
    width: 32;
    static: track_stage1;
    instance_count: 32;
}

register valid_bit_stage1 {
    width: 1;
    static: track_stage1;
    instance_count: 32;
}

action do_stage1(){
    // first table stage
    hashpipe_meta.mKeyCarried = ipv4.srcAddr;
    hashpipe_meta.mCountCarried = 0;

    // hash using my custom function 
    modify_field_with_hash_based_offset(hashpipe_meta.mIndex, 0, stage1_hash,
    32);

    // read the key and value at that location
    hashpipe_meta.mKeyInTable = flow_tracker_stage1[hashpipe_meta.mIndex];
    hashpipe_meta.mCountInTable = packet_counter_stage1[hashpipe_meta.mIndex];
    hashpipe_meta.mValid = valid_bit_stage1[hashpipe_meta.mIndex];

    // check if location is empty or has a differentkey in there
    hashpipe_meta.mKeyInTable = (hashpipe_meta.mValid == 0)? hashpipe_meta.mKeyCarried : hashpipe_meta.mKeyInTable;
    hashpipe_meta.mDiff = (hashpipe_meta.mValid == 0)? 0 : hashpipe_meta.mKeyInTable - hashpipe_meta.mKeyCarried;

    // update hash table
    flow_tracker_stage1[hashpipe_meta.mIndex] = ipv4.srcAddr;
    packet_counter_stage1[hashpipe_meta.mIndex] = ((hashpipe_meta.mDiff == 0)?
    hashpipe_meta.mCountInTable + 1 : 1);
    valid_bit_stage1[hashpipe_meta.mIndex] = 1;

    // update metadata carried to the next table stage
    hashpipe_meta.mKeyCarried = ((hashpipe_meta.mDiff == 0) ? 0:
    hashpipe_meta.mKeyInTable);
    hashpipe_meta.mCountCarried = ((hashpipe_meta.mDiff == 0) ? 0:
    hashpipe_meta.mCountInTable);  
}

table track_stage1 {
    actions { do_stage1; }
    size: 0;
}

/********************** table stage 2 **************************/

register flow_tracker_stage2 {
    width: 32;
    static: track_stage2;
    instance_count: 32;
}

register packet_counter_stage2 {
    width: 32;
    static: track_stage2;
    instance_count: 32;
}

register valid_bit_stage2 {
    width: 1;
    static: track_stage2;
    instance_count: 32;
}

action do_stage2(){
    // hash packet using stage 2 hash function 
    modify_field_with_hash_based_offset(hashpipe_meta.mIndex, 0, stage2_hash,
    32);

    // find packet key in table
    hashpipe_meta.mKeyInTable = flow_tracker_stage2[hashpipe_meta.mIndex];
    hashpipe_meta.mCountInTable = packet_counter_stage2[hashpipe_meta.mIndex];
    hashpipe_meta.mValid = valid_bit_stage2[hashpipe_meta.mIndex];

    // check if table has a different key
    hashpipe_meta.mKeyInTable = (hashpipe_meta.mValid == 0)? hashpipe_meta.mKeyCarried : hashpipe_meta.mKeyInTable;
    hashpipe_meta.mDiff = (hashpipe_meta.mValid == 0)? 0 : hashpipe_meta.mKeyInTable - hashpipe_meta.mKeyCarried;

    // update hash table
    flow_tracker_stage2[hashpipe_meta.mIndex] = ((hashpipe_meta.mDiff == 0)?
    hashpipe_meta.mKeyInTable : ((hashpipe_meta.mCountInTable <
    hashpipe_meta.mCountCarried) ? hashpipe_meta.mKeyCarried :
    hashpipe_meta.mKeyInTable));

    packet_counter_stage2[hashpipe_meta.mIndex] = ((hashpipe_meta.mDiff == 0)?
    hashpipe_meta.mCountInTable + hashpipe_meta.mCountCarried :
    ((hashpipe_meta.mCountInTable < hashpipe_meta.mCountCarried) ?
    hashpipe_meta.mCountCarried : hashpipe_meta.mCountInTable));

    valid_bit_stage2[hashpipe_meta.mIndex] = ((hashpipe_meta.mValid == 0) ?
    ((hashpipe_meta.mKeyCarried == 0) ? (bit<1>)0 : 1) : (bit<1>)1);

    // update metadata carried to the next table stage
    hashpipe_meta.mKeyCarried = ((hashpipe_meta.mDiff == 0) ? 0:
    hashpipe_meta.mKeyInTable);
    hashpipe_meta.mCountCarried = ((hashpipe_meta.mDiff == 0) ? 0:
    hashpipe_meta.mCountInTable);  
}

table track_stage2 {
    actions { do_stage2; }
    size: 0;
}
       
