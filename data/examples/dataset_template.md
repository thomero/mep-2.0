# Dataset Template for YOLO Training

```
data/mep/
  images/
    train/
      plan_001_0.png
    val/
      plan_101_0.png
  labels/
    train/
      plan_001_0.txt
    val/
      plan_101_0.txt
```

Each label file follows YOLO format:

```
<class_index> <x_center_norm> <y_center_norm> <width_norm> <height_norm>
```

Use the class ordering defined in `app/ai/models/classes.txt`.
