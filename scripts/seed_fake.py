import random
from datetime import datetime, timedelta

random.seed(42)

PROGRAMS = ['Statistika','Matematika','Fisika','Kimia','Biologi','Teknik Geofisika']
FEMALE_FIRST = ['Siti','Ayu','Dewi','Nadia','Putri','Rani','Maya','Aulia','Nisa','Intan']
MALE_FIRST = ['Agus','Budi','Dimas','Eko','Fajar','Rizky','Rafi','Adi','Yoga','Bayu']
LAST = ['Saputra','Santoso','Wijaya','Hidayat','Pratama','Nugroho','Ramadhan','Maulana','Hakim','Firmansyah']
STREET = ['Jl. Merpati','Jl. Kenari','Jl. Pahlawan','Jl. Sudirman','Jl. Ahmad Yani','Jl. Rajawali','Jl. Nusa Indah','Jl. Anggrek']

def rand_phone():
    # Simple Indonesian-like phone, 10-13 digits starting with 08
    length = random.randint(10, 13)
    return "08" + "".join(str(random.randint(0,9)) for _ in range(length-2))

def rand_created_at():
    # Random date within last 18 months
    months = 18
    days_back = random.randint(0, months*30)
    dt = datetime.now() - timedelta(days=days_back, hours=random.randint(0,23), minutes=random.randint(0,59))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def generate(n=200, start_year=2018, end_year=2025):
    rows = []
    for i in range(n):
        gender = random.choice(['L','P'])
        first = random.choice(MALE_FIRST if gender=='L' else FEMALE_FIRST)
        last = random.choice(LAST)
        nama = f"{first} {last}"
        angkatan = random.randint(start_year, end_year)
        prodi = random.choice(PROGRAMS)
        stambuk = f"{angkatan}{random.randint(100000, 999999)}"
        alamat = f"{random.choice(STREET)} No.{random.randint(1,200)}, Kota {random.choice(['Makassar','Palu','Kendari','Manado','Gorontalo'])}"
        rows.append({
            'stambuk': stambuk,
            'nama': nama,
            'jenis_kelamin': gender,
            'program_studi': prodi,
            'no_hp': rand_phone(),
            'angkatan': angkatan,
            'alamat': alamat,
            'created_at': rand_created_at(),
        })
    return rows

def write_seed_sql(rows, path='sql/seed.sql'):
    header = "USE brm;\nINSERT INTO tb_mahasiswa_brm (stambuk,nama,jenis_kelamin,program_studi,no_hp,angkatan,alamat,created_at) VALUES\n"
    values = []
    for r in rows:
        v = f"(\'{r['stambuk']}\', \'{r['nama']}\', \'{r['jenis_kelamin']}\', \'{r['program_studi']}\', \'{r['no_hp']}\', {r['angkatan']}, \'{r['alamat']}\', \'{r['created_at']}\')"
        values.append(v)
    sql = header + ",\n".join(values) + ";\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(sql)

if __name__ == "__main__":
    rows = generate(200)
    import os
    # If run from repo root
    out = 'sql/seed.sql'
    if not os.path.exists('sql'):
        os.makedirs('sql', exist_ok=True)
    write_seed_sql(rows, out)
    print(f"Generated {out} with {len(rows)} rows.")
