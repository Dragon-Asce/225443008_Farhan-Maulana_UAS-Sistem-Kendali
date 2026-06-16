"""
╔══════════════════════════════════════════════════════════════════╗
║  UAS SISTEM KENDALI – GENAP 2025/2026                            ║
║  Nama           : Farhan Maulana                                 ║
║  NIM            : 225443008                                      ║
║  Kelas          : 1AEC-1                                         ║
║  Nomor Absen    : 8                                              ║
║  Dosen Pengampu : Abdur Rohman Harits Martawireja, S.Si., M.T.   ║
║  Mata Kuliah    : Sistem Kendali                                 ║
╚══════════════════════════════════════════════════════════════════╝

PENJELASAN LIBRARY YANG DIGUNAKAN:
─────────────────────────────────────────────────────────────────
  NumPy    : Library komputasi numerik untuk array, matematika,
             dan operasi vektor/matriks.
  Matplotlib: Library visualisasi grafik 2D/3D yang menghasilkan
             plot interaktif maupun statis.
  control  : Python Control System Library – digunakan untuk
             membuat fungsi transfer, simulasi step response,
             analisis pole/zero, dan feedback system.
─────────────────────────────────────────────────────────────────
"""

import numpy as np
import matplotlib.pyplot as plt
import control

# ================================================================
# SOAL 1 – PENENTUAN PARAMETER SISTEM
# ================================================================
print("=" * 60)
print("  SOAL 1 – PENENTUAN PARAMETER SISTEM")
print("=" * 60)

NIM_last = 8   # Angka terakhir NIM 225443008
absen    = 8   # Nomor absen = 8

A   = NIM_last           # A  = 8
B   = NIM_last / absen   # B  = 8/8 = 1.0
K   = A                  # K  = 8
tau = 1.0 / B            # τ  = 1/1 = 1.0 s

print(f"\n  a. Nilai Parameter:")
print(f"     A = Angka Akhir NIM          = {A}")
print(f"     B = Angka Akhir NIM / Absen  = {NIM_last}/{absen} = {B:.4f}")
print(f"\n  b. Nilai K dan τ:")
print(f"     K = A = {K}")
print(f"     τ = 1/B = 1/{B:.4f} = {tau:.4f} s")
print(f"\n  c. Model Fungsi Transfer:")
print(f"                  {K}")
print(f"     G(s)  =  ─────────────")
print(f"               {tau}s  +  1")


# ================================================================
# SOAL 2 – ANALISIS SISTEM OPEN LOOP
# ================================================================
print("\n" + "=" * 60)
print("  SOAL 2 – ANALISIS SISTEM OPEN LOOP")
print("=" * 60)

# a. Buat model fungsi transfer menggunakan library control
#    control.tf(numerator, denominator) membuat objek Transfer Function
G = control.tf([K], [tau, 1])

# b. Tampilkan fungsi transfer
print("\n  a-b. Fungsi Transfer Open Loop G(s):")
print(G)

# c. Simulasi step response (input 1 Volt = step unit)
t = np.linspace(0, 15, 2000)   # waktu simulasi 0 – 15 detik
t_ol, y_ol = control.step_response(G, T=t)

# d. Hitung steady-state, pole, time constant
ss_ol    = float(y_ol[-1])
poles_ol = control.poles(G)
print(f"\n  d. Analisis Open Loop:")
print(f"     Steady-State Value : {ss_ol:.4f} cm")
print(f"     Pole Sistem        : {poles_ol}")
print(f"     Time Constant (τ)  : {tau:.4f} s")
print(f"\n     ▶ Pole berada di s = {poles_ol[0].real:.1f} (real negatif)")
print(f"       → Sistem STABIL karena pole di kiri bidang-s")

# e. Hubungan letak pole dan kecepatan respon
print(f"\n  e. Hubungan Pole dan Kecepatan Respon:")
print(f"     Pole semakin jauh ke kiri (nilai real makin negatif)")
print(f"     → sistem merespons lebih CEPAT (time constant lebih kecil)")
print(f"     Pole = {poles_ol[0].real:.1f}  ↔  τ = 1/|pole| = {1/abs(poles_ol[0].real):.4f} s")


# ================================================================
# SOAL 3 – ANALISIS SISTEM CLOSED LOOP
# ================================================================
print("\n" + "=" * 60)
print("  SOAL 3 – ANALISIS SISTEM CLOSED LOOP")
print("=" * 60)


T_manual_num = [K]
T_manual_den = [tau, 1 + K]
print(f"\n  c. Manual Derivasi Fungsi Transfer Closed Loop:")
print(f"           G(s)              {K}/(τs+1)")
print(f"  T(s) = ────────── = ─────────────────────────")
print(f"          1 + G(s)       1 + {K}/(τs+1)")
print(f"\n             {K}")
print(f"       = ───────────────")
print(f"          τs + 1 + {K}")
print(f"\n             {K}")
print(f"       = ─────────────  (τ={tau}, K={K})")
print(f"          {tau}s + {1+K}")

# d. Buat model closed loop pada Python
#    control.feedback(G, 1) = G/(1+G) untuk unity feedback
T = control.feedback(G, 1)
print(f"\n  d. Fungsi Transfer Closed Loop [Python]:")
print(T)

# e. Simulasi step response closed loop
t_cl, y_cl = control.step_response(T, T=t)
ss_cl = float(y_cl[-1])
poles_cl = control.poles(T)
print(f"\n     Pole Closed Loop: {poles_cl}")
print(f"     Steady-State CL : {ss_cl:.4f}")

# f. Perbandingan OL vs CL
def get_metrics(t_arr, y_arr):
    """Hitung rise time, settling time, overshoot, peak time, steady-state."""
    ss = float(y_arr[-1])
    idx10 = np.where(y_arr >= 0.1 * ss)[0]
    idx90 = np.where(y_arr >= 0.9 * ss)[0]
    rt = float(t_arr[idx90[0]] - t_arr[idx10[0]]) if len(idx10) and len(idx90) else float('nan')
    band   = 0.02 * ss
    last_outside = np.where(np.abs(y_arr - ss) > band)[0]
    st = float(t_arr[last_outside[-1]]) if len(last_outside) else 0.0
    peak   = float(np.max(y_arr))
    os_pct = ((peak - ss) / ss * 100) if ss > 0 else 0.0
    pt     = float(t_arr[np.argmax(y_arr)])
    return dict(rise_time=rt, settling_time=st, overshoot=os_pct,
                peak_time=pt, ss=ss)

m_ol = get_metrics(t_ol, y_ol)
m_cl = get_metrics(t_cl, y_cl)

print(f"\n  f. Perbandingan Respon Open Loop vs Closed Loop:")
print(f"  {'Karakteristik':<22} {'Open Loop':>12} {'Closed Loop':>12}")
print(f"  {'-'*46}")
print(f"  {'Rise Time (s)':<22} {m_ol['rise_time']:>12.4f} {m_cl['rise_time']:>12.4f}")
print(f"  {'Settling Time (s)':<22} {m_ol['settling_time']:>12.4f} {m_cl['settling_time']:>12.4f}")
print(f"  {'Steady-State':<22} {m_ol['ss']:>12.4f} {m_cl['ss']:>12.4f}")


# ================================================================
# SOAL 4 – PID ZIEGLER-NICHOLS
# ================================================================
print("\n" + "=" * 60)
print("  SOAL 4 – PENALAAN PID ZIEGLER-NICHOLS")
print("=" * 60)

Ku = A + 2       # Gain kritis = 8 + 2 = 10
Pu = tau         # Periode osilasi = τ = 1.0

# a. Parameter PID
Kp = 0.6  * Ku      # = 6.0
Ti = 0.5  * Pu      # = 0.5
Td = 0.125 * Pu     # = 0.125

# b. Nilai Ki dan Kd
Ki = Kp / Ti         # = 12.0
Kd = Kp * Td         # = 0.75

print(f"\n  Gain Kritis  Ku = A+2 = {A}+2 = {Ku}")
print(f"  Periode Osilasi Pu = τ = {Pu}")
print(f"\n  a. Parameter PID Ziegler-Nichols:")
print(f"     Kp = 0.6 × Ku  = 0.6 × {Ku}   = {Kp:.2f}")
print(f"     Ti = 0.5 × Pu  = 0.5 × {Pu}  = {Ti}")
print(f"     Td = 0.125 × Pu = 0.125 × {Pu} = {Td}")
print(f"\n  b. Ki dan Kd:")
print(f"     Ki = Kp/Ti = {Kp:.2f}/{Ti} = {Ki}")
print(f"     Kd = Kp×Td = {Kp:.2f}×{Td} = {Kd}")
print(f"\n  c. Fungsi Transfer PID:")
print(f"                   {Ki}           ")
print(f"     C(s) = {Kp:.2f} + ─── + {Kd}s")
print(f"                    s            ")
print(f"\n  d. Fungsi masing-masing parameter:")
print(f"     Kp = {Kp}  → Mempercepat respons, mengurangi rise time")
print(f"                  namun dapat menyebabkan overshoot")
print(f"     Ki = {Ki}  → Menghilangkan error steady-state (SSE = 0)")
print(f"                  namun dapat memperlambat respons")
print(f"     Kd = {Kd}  → Meredam osilasi dan overshoot,")
print(f"                  meningkatkan stabilitas transien")


# ================================================================
# SOAL 5 – SIMULASI SISTEM DENGAN KENDALI PID
# ================================================================
print("\n" + "=" * 60)
print("  SOAL 5 – SIMULASI SISTEM DENGAN KENDALI PID")
print("=" * 60)

# b. Model PID: C(s) = Kd*s^2 + Kp*s + Ki  /  s
#    (dalam bentuk transfer function)
C = control.tf([Kd, Kp, Ki], [1, 0])
print(f"\n  b. Fungsi Transfer PID C(s):")
print(C)

# c. Sistem PID closed loop
#    T_pid(s) = C(s)G(s) / (1 + C(s)G(s))
T_pid = control.feedback(C * G, 1)
print(f"\n  c. Fungsi Transfer Closed Loop + PID T_pid(s):")
print(T_pid)

# d. Simulasi step response
t_pid, y_pid = control.step_response(T_pid, T=t)
m_pid = get_metrics(t_pid, y_pid)

# f. Tabel perbandingan ketiga sistem
print(f"\n  f. Tabel Perbandingan Performa Ketiga Sistem:")
print(f"  {'Karakteristik':<22} {'Open Loop':>12} {'Closed Loop':>12} {'PID':>12}")
print(f"  {'-'*60}")
print(f"  {'Rise Time (s)':<22} {m_ol['rise_time']:>12.4f} {m_cl['rise_time']:>12.4f} {m_pid['rise_time']:>12.4f}")
print(f"  {'Settling Time (s)':<22} {m_ol['settling_time']:>12.4f} {m_cl['settling_time']:>12.4f} {m_pid['settling_time']:>12.4f}")
print(f"  {'Overshoot (%)':<22} {m_ol['overshoot']:>12.4f} {m_cl['overshoot']:>12.4f} {m_pid['overshoot']:>12.4f}")
print(f"  {'Peak Time (s)':<22} {m_ol['peak_time']:>12.4f} {m_cl['peak_time']:>12.4f} {m_pid['peak_time']:>12.4f}")
print(f"  {'Steady-State Value':<22} {m_ol['ss']:>12.4f} {m_cl['ss']:>12.4f} {m_pid['ss']:>12.4f}")


# ================================================================
# SOAL 6 – ANALISIS HASIL
# ================================================================
print("\n" + "=" * 60)
print("  SOAL 6 – ANALISIS HASIL")
print("=" * 60)
print("""
  a. Pengaruh Umpan Balik (Feedback) terhadap sistem:
     Feedback memungkinkan sistem mengoreksi dirinya sendiri
     berdasarkan selisih antara setpoint dan output aktual.
     Pada closed loop:
     • Time constant lebih kecil → respons lebih cepat
     • Steady-state lebih dekat ke setpoint (namun ada offset
       pada proportional-only karena gain tidak tak hingga)
     • Sistem lebih robust terhadap gangguan eksternal

  b. Pengaruh PID terhadap kecepatan respons:
     PID secara signifikan mempercepat respons sistem:
     • Rise Time dari {:.3f}s (OL) → {:.3f}s (PID)
     • Settling Time dari {:.3f}s (OL) → {:.3f}s (PID)
     Hal ini disebabkan oleh aksi Kp yang memperkuat sinyal
     error, dan Kd yang meredam osilasi.

  c. Pengaruh PID terhadap error steady-state:
     Aksi integral (Ki) menghilangkan error steady-state.
     • SS Open Loop  = {:.4f} cm (target 1, error = {:.4f})
     • SS Closed Loop = {:.4f} cm (error = {:.4f})
     • SS PID         = {:.4f} cm (error ≈ 0)

  d. Apakah respon mengalami overshoot?
     PID mengalami overshoot kecil = {:.2f}%.
     Penyebabnya: aksi integral mengakumulasi error dan
     mendorong output melampaui setpoint sesaat, sebelum
     aksi derivatif meredam dan sistem stabil di setpoint.

  e. Pengaruh masing-masing parameter PID:
     • Kp (Proporsional) : Mempercepat respons, mengurangi
       rise time. Nilai terlalu besar → osilasi/instabil.
     • Ki (Integral)     : Menghilangkan SSE. Nilai terlalu
       besar → overshoot besar dan respons lambat mengendap.
     • Kd (Derivatif)    : Meredam osilasi dan overshoot,
       meningkatkan stabilitas. Sensitif terhadap noise.
""".format(
    m_ol['rise_time'],  m_pid['rise_time'],
    m_ol['settling_time'], m_pid['settling_time'],
    m_ol['ss'],  1 - m_ol['ss'],
    m_cl['ss'],  1 - m_cl['ss'],
    m_pid['ss'],
    m_pid['overshoot']
))


# ================================================================
# PLOT 1 – OPEN LOOP STEP RESPONSE
# ================================================================
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(t_ol, y_ol, 'b-', linewidth=2.5, label='Respon Open Loop')
ax1.axhline(ss_ol, color='gray', linestyle='--', linewidth=1.5,
            label=f'Steady-State = {ss_ol:.2f} cm')
ax1.set_title(f'Respon Step Open Loop  |  G(s) = {K}/(s+1)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Waktu (s)', fontsize=11)
ax1.set_ylabel('Posisi Aktuator y(t) [cm]', fontsize=11)
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_xlim([0, 15])
plt.tight_layout()
plt.savefig('plot1_openloop.png', dpi=150, bbox_inches='tight')
plt.close()

# ================================================================
# PLOT 2 – S-PLANE POLE-ZERO MAP
# ================================================================
fig2, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, sys_, title_ in zip(axes, [G, T], ['Open Loop G(s)', 'Closed Loop T(s)']):
    poles_ = control.poles(sys_)
    ax.axhline(0, color='k',  lw=0.8); ax.axvline(0, color='k', lw=0.8)
    for p in poles_:
        ax.plot(p.real, p.imag, 'rx', markersize=14, markeredgewidth=2.5, label='Pole')
        ax.annotate(f'  s = {p.real:.2f}', xy=(p.real, p.imag), fontsize=9, color='red')
    ax.set_xlim([-12, 2]); ax.set_ylim([-2, 2])
    ax.set_title(f'S-Plane – {title_}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Bagian Real', fontsize=10); ax.set_ylabel('Bagian Imajiner', fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, linestyle='--', alpha=0.6)
plt.suptitle('Peta Pole (S-Plane)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('plot2_splane.png', dpi=150, bbox_inches='tight')
plt.close()

# ================================================================
# PLOT 3 – OPEN LOOP vs CLOSED LOOP
# ================================================================
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(t_ol, y_ol, 'b-',  lw=2.5, label='Respon Open Loop')
ax3.plot(t_cl, y_cl, 'g--', lw=2.5, label='Respon Closed Loop')
ax3.axhline(1, color='k', linestyle=':', lw=1.5, label='Setpoint = 1')
ax3.set_title('Perbandingan: Open Loop vs Closed Loop', fontsize=13, fontweight='bold')
ax3.set_xlabel('Waktu (s)', fontsize=11); ax3.set_ylabel('y(t) [cm]', fontsize=11)
ax3.legend(fontsize=10); ax3.grid(True, linestyle='--', alpha=0.6)
ax3.set_xlim([0, 15])
plt.tight_layout()
plt.savefig('plot3_ol_vs_cl.png', dpi=150, bbox_inches='tight')
plt.close()

# ================================================================
# PLOT 4 – OPEN LOOP + CLOSED LOOP + PID
# ================================================================
fig4, ax4 = plt.subplots(figsize=(11, 6))
ax4.plot(t_ol,  y_ol,  'b-',  lw=2.5, label='Respon Open Loop')
ax4.plot(t_cl,  y_cl,  'g--', lw=2.5, label='Respon Closed Loop')
ax4.plot(t_pid, y_pid, 'r-',  lw=2.5, label='Respon Closed Loop + PID')
ax4.axhline(1, color='k', linestyle=':', lw=1.5, label='Setpoint = 1 cm')
ax4.set_title('Perbandingan Respon Step:\nOpen Loop | Closed Loop | Closed Loop + PID',
              fontsize=13, fontweight='bold')
ax4.set_xlabel('Waktu (s)', fontsize=11)
ax4.set_ylabel('Posisi Aktuator y(t) [cm]', fontsize=11)
ax4.legend(fontsize=10); ax4.grid(True, linestyle='--', alpha=0.6)
ax4.set_xlim([0, 15]); ax4.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig('plot4_all.png', dpi=150, bbox_inches='tight')
plt.close()

# ================================================================
# PLOT 5 – BAR CHART PERBANDINGAN PERFORMA
# ================================================================
fig5, ax5 = plt.subplots(figsize=(9, 5))
cats = ['Rise Time (s)', 'Settling Time (s)', 'Steady-State Value']
vals_ol  = [m_ol['rise_time'],  m_ol['settling_time'],  m_ol['ss']]
vals_cl  = [m_cl['rise_time'],  m_cl['settling_time'],  m_cl['ss']]
vals_pid = [m_pid['rise_time'], m_pid['settling_time'], m_pid['ss']]
x = np.arange(len(cats)); w = 0.25
for bars, vals, lbl, clr in zip(
        [ax5.bar(x-w, vals_ol, w), ax5.bar(x, vals_cl, w), ax5.bar(x+w, vals_pid, w)],
        [vals_ol, vals_cl, vals_pid],
        ['Open Loop', 'Closed Loop', 'PID'],
        ['steelblue', 'seagreen', 'tomato']):
    bars.set_label(lbl);
    
    for bar in bars:
        bar.set_color(clr)
        h = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2, h + 0.01, f'{h:.3f}',
                 ha='center', va='bottom', fontsize=8)
ax5.set_title('Perbandingan Performa Sistem', fontsize=13, fontweight='bold')
ax5.set_xticks(x); ax5.set_xticklabels(cats, fontsize=10)
ax5.set_ylabel('Nilai', fontsize=11)
ax5.legend(fontsize=10); ax5.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot5_metrics.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ SELESAI – Semua plot tersimpan!")
