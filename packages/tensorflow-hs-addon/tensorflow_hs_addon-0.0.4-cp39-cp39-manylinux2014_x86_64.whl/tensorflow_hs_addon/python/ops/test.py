import sys
import pickle
import tensorflow as tf
import numpy as np
# from tensorflow.python.framework import load_library
# lib = load_library.load_op_library("./_reco_ops.so")
# print(dir(lib))

try:
    from tensorflow_hs_addon.python.ops.reco_ops import isin, pooling_by_slots, feature_vec_to_segments, unsorted_feature_vec_to_segments, parse_feature_vec
except ImportError as e:
    from reco_ops import isin, pooling_by_slots, feature_vec_to_segments, unsorted_feature_vec_to_segments, parse_feature_vec


tfv1 = tf.compat.v1
tfv1.disable_v2_behavior()

sess = tfv1.Session()


with open("batches.pkl", 'rb') as f:
    batches = pickle.load(f)

all_fids = set()
for batch in batches:
    all_fids.update(*list(batch['fids']))
fids_lookup_keys = []
fids_lookup_values = []
for i, fid in enumerate(all_fids):
    fids_lookup_keys.append(fid)
    fids_lookup_values.append(i)
fid_lookup = tf.lookup.StaticHashTable(
    tf.lookup.KeyValueTensorInitializer(
        fids_lookup_keys, fids_lookup_values, key_dtype=tf.int64, value_dtype=tf.int32
    ), 0
)

slot_ids_to_pool = [1,
                    2,
                    3,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    20,
                    56,
                    57,
                    60,
                    61,
                    62,
                    63,
                    65,
                    66,
                    67,
                    70,
                    72,
                    76,
                    90,
                    91,
                    92,
                    95,
                    451,
                    452,
                    453,
                    454]
full_embs = tf.constant(np.random.rand(len(all_fids), 8), dtype=tf.float32)


def pool_embedings_v1(fids, fid_weights, slot_ids_to_pool):
    ns = "pool_v1"
    with tf.name_scope(ns + "/proc"):
        fid_slots = tf.cast(
            tf.bitwise.right_shift(fids, 53), tf.int32, name="fid_slots"
        )
        is_valid = isin(fid_slots, slot_ids_to_pool)
        valid_fids = tf.where(is_valid, fids, 0, name="filter")
        flat_fids = tf.reshape(valid_fids, (-1,))
        unique_fids, flat_indices = tf.unique(flat_fids, name="fid_dedup")
        fid_indices = tf.reshape(flat_indices, tf.shape(
            valid_fids), name="fid_indices")

    unique_fid_indices = fid_lookup.lookup(unique_fids)
    unique_embs = tf.gather(full_embs, unique_fid_indices)

    with tf.name_scope(ns + "/calc"):
        res, _ = pooling_by_slots(fid_indices, fid_slots,
                                  fid_weights, unique_embs, slot_ids_to_pool)
    return res


def pool_embeddings_unsorted(fids, fid_weights, query_slots):
    ns = "pool_segmented"
    with tf.name_scope(ns + "/proc"):
        fid_slots = tf.cast(
            tf.bitwise.right_shift(fids, 53), tf.int32, name="fid_slots"
        )
        valid_fids = tf.where(isin(fid_slots, slot_ids_to_pool), fids, 0)
        flat_fids = tf.reshape(valid_fids, (-1,))
        unique_fids, flat_indices = tf.unique(flat_fids, name="fid_dedup")

        fid_indices = tf.reshape(flat_indices, tf.shape(
            valid_fids), name="fid_indices")

        segment_ids, indices, weights = unsorted_feature_vec_to_segments(
            fid_indices, fid_slots, fid_weights, query_slots
        )
    unique_fid_indices = fid_lookup.lookup(unique_fids)
    embs = tf.gather(full_embs, unique_fid_indices)

    with tf.name_scope(ns + "/calc"):
        bs = tf.shape(fid_indices)[0]
        gathered = tf.gather(embs, indices)
        gathered *= tf.expand_dims(weights, -1)
        pooled_embeddings_spread = tf.math.unsorted_segment_sum(
            gathered, segment_ids, bs * len(query_slots))

        batch_size = tf.shape(fid_indices)[0]
        dim = embs.shape[-1]

        print("pool spread shape", pooled_embeddings_spread.shape)
        pooled_embeddings = tf.reshape(pooled_embeddings_spread,
                                       [batch_size, len(query_slots), dim])

        print("pool", pooled_embeddings)
        return pooled_embeddings


def pool_embeddings_v4(fids, fid_weights, query_slots):
    ns = "pool_new"
    with tf.name_scope(ns + "/proc"):
        print("start parse")
        segment_ids, indices, weights, unique_fids = parse_feature_vec(
            fids, fid_weights, query_slots)
        print("parse done")
        # segment_ids, indices, weights, num_valid_entries, unique_fids = parse_feature_vec(
        #     fids, fid_weights, query_slots)
        # print("parse done")
        # segment_ids = segment_ids[:num_valid_entries]
        # indices = indices[:num_valid_entries]
        # weights = weights[:num_valid_entries]

    unique_fid_indices = fid_lookup.lookup(unique_fids)
    embs = tf.gather(full_embs, unique_fid_indices)

    with tf.name_scope(ns + "/calc"):
        bs = tf.shape(fids)[0]

        gathered = tf.gather(embs, indices)
        gathered *= tf.expand_dims(weights, -1)
        pooled_embeddings_spread = tf.math.unsorted_segment_sum(
            gathered, segment_ids, bs * len(query_slots))

        batch_size = tf.shape(fids)[0]
        dim = embs.shape[-1]

        print("pool spread shape", pooled_embeddings_spread.shape)
        pooled_embeddings = tf.reshape(pooled_embeddings_spread,
                                       [batch_size, len(query_slots), dim])

        print("pool", pooled_embeddings)
        return pooled_embeddings


fids = tfv1.placeholder(tf.int64, [None, None])
fid_weights = tfv1.placeholder(tf.float32, [None, None])

pv1 = pool_embedings_v1(fids, fid_weights, slot_ids_to_pool)
pv2 = pool_embeddings_unsorted(fids, fid_weights, slot_ids_to_pool)
pv3 = pool_embeddings_v4(fids, fid_weights, slot_ids_to_pool)
print("v1 result", pv1)
print("v2 result", pv2)
print("v3 result", pv3)

test_empty = pool_embeddings_v4(fids, fid_weights, [1001])

res = tf.reduce_max(tf.abs(pv1 - pv2))
res2 = tf.reduce_max(tf.abs(pv1 - pv3))

sess_config = tfv1.ConfigProto()
sess_config.intra_op_parallelism_threads = 1
sess_config.inter_op_parallelism_threads = 1
sess = tfv1.Session(config=sess_config)
sess.run(tfv1.tables_initializer())
sess.run(tfv1.global_variables_initializer())

# for batch in batches[:100]:
#     d1, d2 = sess.run((res, res2), feed_dict={
#         fids: batch['fids'],
#         fid_weights: batch["fid_weights"]
#     })
#     print("diff", d1, d2)

test_empty_res = sess.run(test_empty,  feed_dict={
    fids: batches[0]['fids'],
    fid_weights: batches[0]["fid_weights"]
})
print(test_empty_res[:3])


tf.profiler.experimental.start("./bench_log")
for i in range(30):
    for batch in batches:
        _ = sess.run((pv3,), feed_dict={
            fids: batch['fids'],
            fid_weights: batch["fid_weights"]
        })
tf.profiler.experimental.stop()
