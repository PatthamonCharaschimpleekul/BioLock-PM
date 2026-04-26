import cadquery as cq

# --- Global Configuration ---
PITCH = 16.6
DEPTH = 25.0
THICKNESS = 5.0     # ความหนาใยสับปะรด PALF
WALL = 5.0          # ความหนาผนังโครง
CLEARANCE = 0.8     # ระยะเผื่อสไลด์
HEIGHT = 510.0      # ความสูงแผงคอยล์ร้อน

def create_filter_set(width, height):
    # 1. คำนวณความกว้างจีบ และประกาศตัวแปรให้ชัดเจน
    num_pleats = int(width / PITCH)
    # ใช้ชื่อตัวแปรเดียวให้จบในฟังก์ชันเพื่อกันความสับสน
    p_width = (num_pleats * PITCH) + THICKNESS
    
    # --- Part A: Filter Media (ใยสับปะรดสำหรับ Simulation) ---
    pts = [(0, 0)]
    for i in range(num_pleats):
        pts.append(((i * PITCH) + PITCH/2, DEPTH))
        pts.append(((i * PITCH) + PITCH, 0))
    
    media = (
        cq.Workplane("XY")
        .polyline(pts)
        .offset2D(THICKNESS)
        .extrude(height - (WALL * 2) - 2) 
    )
    # ใช้ p_width ที่ประกาศไว้ด้านบน
    media = media.translate((-p_width/2, -height/2 + WALL + 1, 0))

    # --- Part B: Inner Frame (ตลับพยุงฟิลเตอร์) ---
    # ใช้ p_width ในการกำหนดขนาดกรอบ
    inner_frame = (
        cq.Workplane("XY")
        .rect(p_width + (WALL * 2), height)
        .rect(p_width, height - (WALL * 2)) 
        .extrude(THICKNESS + 2)
    )

    # --- Part C: Outer Rail (รางล็อกแปะเครื่อง) ---
    rail_total_w = p_width + (WALL * 2) + (CLEARANCE * 2) + (WALL * 2)
    outer_rail = (
        cq.Workplane("XY")
        .box(rail_total_w, height + (WALL * 2), THICKNESS + 10)
        # เจาะร่องสไลด์ (Sliding Groove)
        .faces(">Z").workplane()
        .rect(p_width + (WALL * 2) + (CLEARANCE * 2), height + CLEARANCE)
        .cutThruAll()
        # เจาะรูทางลมหลัก
        .faceecs(">Z").workplane()
        .rt(p_width, height - (WALL * 2))
        .cutThruAll()
        # เปิดด้านข้างเพื่อให้สไลด์ตลับเข้าได้
        .faces(">X").workplane()
        .rect(THICKNESS + 20, height + CLEARANCE)
        .cutThruAll()
    )

    return media, inner_frame, outer_rail

# --- การรันและ Export ทั้ง 6 ไฟล์ ---

# 1. ชุดแผงหลัง (Rear - 760mm)
rear_w = 760.0
r_media, r_inner, r_outer = create_filter_set(rear_w, HEIGHT)
cq.exporters.export(r_media, '1_Media_Rear_760.stl')
cq.exporters.export(r_inner, '2_InnerFrame_Rear_760.stl')
cq.exporters.export(r_outer, '3_OuterRail_Rear_760.stl')

# 2. ชุดแผงข้าง (Side - 260mm)
side_w = 260.0
s_media, s_inner, s_outer = create_filter_set(side_w, HEIGHT)
cq.exporters.export(s_media, '4_Media_Side_260.stl')
cq.exporters.export(s_inner, '5_InnerFrame_Side_260.stl')
cq.exporters.export(s_outer, '6_OuterRail_Side_260.stl')

print("Successfully generated all 6 files without variable errors.")