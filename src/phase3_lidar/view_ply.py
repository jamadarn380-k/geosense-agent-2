import open3d as o3d

PLY_FILE = "outputs/point_clouds/study_area_colored.ply"

pcd = o3d.io.read_point_cloud(PLY_FILE)

print(f"Loaded point cloud: {PLY_FILE}")
print(pcd)

o3d.visualization.draw_geometries([pcd])