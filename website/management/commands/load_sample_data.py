import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfile
from courses.models import Subject, Course
from teachers.models import Teacher
from batches.models import Batch
from students.models import Student
from timetable.models import TimetableEntry
from attendance.models import Attendance
from fees.models import FeeRecord
from enquiries.models import AdmissionEnquiry, ContactMessage
from materials.models import StudyMaterial
from announcements.models import Announcement
from website.models import Gallery, Testimonial, FAQ


class Command(BaseCommand):
    help = 'Populates the database with realistic sample data for NS Classes coaching institute'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Beginning sample data generation for NS Classes...'))

        # 1. Super Admin / Director User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'directors@nsclasses.edu',
                'first_name': 'Nikhil Kumar',
                'last_name': 'Singh',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Super Admin user: admin / admin123"))

        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'role': 'admin',
                'phone': '987654321',
                'address': 'NS Classes Campus, Main Market Road, Bihar, India'
            }
        )

        # 2. Academic Subjects
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH', 'icon': 'bi-calculator'},
            {'name': 'Physics', 'code': 'PHYS', 'icon': 'bi-lightning-charge-fill'},
            {'name': 'Chemistry', 'code': 'CHEM', 'icon': 'bi-droplet-half'},
            {'name': 'Biology', 'code': 'BIO', 'icon': 'bi-flower1'},
            {'name': 'English Core & Grammar', 'code': 'ENG', 'icon': 'bi-translate'},
            {'name': 'Hindi Literature & Vyakaran', 'code': 'HIN', 'icon': 'bi-book-fill'},
            {'name': 'Science (Physics, Chem, Bio)', 'code': 'SCI', 'icon': 'bi-radioactive'},
            {'name': 'Social Science (History, Civics, Geo)', 'code': 'SST', 'icon': 'bi-globe-central-south-asia'},
        ]
        created_subjects = {}
        for s in subjects_data:
            subj, _ = Subject.objects.get_or_create(code=s['code'], defaults={'name': s['name'], 'icon': s['icon']})
            created_subjects[s['code']] = subj
        self.stdout.write(self.style.SUCCESS(f"Created {len(created_subjects)} Academic Subjects."))

        # 3. Sample Courses (5+ Courses for CBSE & Bihar Board)
        courses_data = [
            {
                'name': 'CBSE Class 10 Foundation & Board Excel',
                'board': 'CBSE',
                'class_level': '10',
                'duration': '1 Year Full Academic Session',
                'fees': 18000,
                'description': 'Comprehensive preparation for CBSE 10th Board Exams. Covers complete Mathematics, Science, and English NCERT syllabus with chapter-wise tests, previous 10-year question papers, and weekly mock exams.',
                'subjects': ['MATH', 'SCI', 'ENG', 'SST']
            },
            {
                'name': 'CBSE Class 12 Science Master Batch (PCM/PCB)',
                'board': 'CBSE',
                'class_level': '12',
                'duration': '1 Year Intensive',
                'fees': 28000,
                'description': 'Rigorous physics, chemistry, mathematics and biology guidance for CBSE Class 12 board toppers. Focuses on theoretical depth, numerical solving, derivations, and board presentation.',
                'subjects': ['PHYS', 'CHEM', 'MATH', 'BIO', 'ENG']
            },
            {
                'name': 'Bihar Board Matric (10th) Topper Batch',
                'board': 'BIHAR',
                'class_level': '10',
                'duration': '1 Year Full Session',
                'fees': 15000,
                'description': 'Specialized BSEB Matric preparation in Hindi and English medium. Dedicated coverage of Mathematics, Vigyan, Samajik Vigyan, Hindi, and Sanskrit/English with model question papers.',
                'subjects': ['MATH', 'SCI', 'SST', 'HIN', 'ENG']
            },
            {
                'name': 'Bihar Board Inter (12th) Science I.Sc Special',
                'board': 'BIHAR',
                'class_level': '12',
                'duration': '1 Year Academic Session',
                'fees': 24000,
                'description': 'Expert coaching for BSEB 12th Board examinations with objective question mastery, 50-mark objective practice, subjective answer writing drills, and laboratory concept workshops.',
                'subjects': ['PHYS', 'CHEM', 'MATH', 'BIO', 'HIN']
            },
            {
                'name': 'CBSE Class 9 Conceptual Foundation Program',
                'board': 'CBSE',
                'class_level': '9',
                'duration': '1 Year Foundation',
                'fees': 16000,
                'description': 'Lays strong concepts in Science and Mathematics for high-school success. Builds foundational concepts necessary for Class 10 board exams and competitive Olympiads.',
                'subjects': ['MATH', 'SCI', 'ENG']
            },
            {
                'name': 'Bihar Board Class 9 Shreshtha Batch',
                'board': 'BIHAR',
                'class_level': '9',
                'duration': '1 Year Program',
                'fees': 13000,
                'description': 'Fundamental conceptual training for Class 9 Bihar Board students ensuring strong base in Math, Science, and Language.',
                'subjects': ['MATH', 'SCI', 'HIN', 'SST']
            }
        ]

        created_courses = {}
        for c in courses_data:
            crs, _ = Course.objects.get_or_create(
                name=c['name'],
                defaults={
                    'board': c['board'],
                    'class_level': c['class_level'],
                    'duration': c['duration'],
                    'fees': c['fees'],
                    'description': c['description'],
                    'is_active': True
                }
            )
            for code in c['subjects']:
                if code in created_subjects:
                    crs.subjects.add(created_subjects[code])
            created_courses[c['name']] = crs
        self.stdout.write(self.style.SUCCESS(f"Created {len(created_courses)} Academic Courses."))

        # 4. Sample Faculty / Teachers (5 Teachers)
        teachers_data = [
            {
                'username': 'pinku_raj',
                'first_name': 'Nikhil',
                'last_name': 'Kumar Singh',
                'email': 'nikhil.singh@nsclasses.edu',
                'teacher_id': 'NS-TCH-001',
                'phone': '987654321',
                'qualification': 'M.Sc. Mathematics, B.Ed. (Gold Medalist)',
                'experience': 14,
                'bio': 'Co-Director of NS Classes with over 14 years of teaching Mathematics to CBSE students. Known for formula shortcut techniques and exam psychology coaching.',
                'specialization': ['MATH']
            },
            {
                'username': 'amit_sharma',
                'first_name': 'Amit',
                'last_name': 'Sharma',
                'email': 'amit.sharma@nsclasses.edu',
                'teacher_id': 'NS-TCH-002',
                'phone': '9876543210',
                'qualification': 'M.Sc. Physics (Delhi University)',
                'experience': 10,
                'bio': 'Senior Physics lecturer specializing in Optics, Electromagnetism, and Mechanics with strong numerical problem solving track record.',
                'specialization': ['PHYS', 'SCI']
            },
            {
                'username': 'priya_verma',
                'first_name': 'Priya',
                'last_name': 'Verma',
                'email': 'priya.verma@nsclasses.edu',
                'teacher_id': 'NS-TCH-003',
                'phone': '9876543211',
                'qualification': 'M.Sc. Chemistry, CSIR-NET',
                'experience': 8,
                'bio': 'Chemistry expert making Organic mechanisms and Physical chemistry numericals easy and intuitive for board aspirants.',
                'specialization': ['CHEM', 'SCI']
            },
            {
                'username': 'rajesh_kumar',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'email': 'rajesh.kumar@nsclasses.edu',
                'teacher_id': 'NS-TCH-004',
                'phone': '9876543212',
                'qualification': 'M.Sc. Zoology, B.Ed.',
                'experience': 11,
                'bio': 'Dedicated Biology faculty focused on diagram accuracy, NCERT line-by-line concept grasp, and BSEB objective answering techniques.',
                'specialization': ['BIO', 'SCI']
            },
            {
                'username': 'sunil_pandey',
                'first_name': 'Sunil',
                'last_name': 'Pandey',
                'email': 'sunil.pandey@nsclasses.edu',
                'teacher_id': 'NS-TCH-005',
                'phone': '9876543213',
                'qualification': 'M.A. English & Hindi Literature',
                'experience': 9,
                'bio': 'Master language educator assisting students in scoring 95+ in English Grammar, Writing sections, and Hindi Vyakaran.',
                'specialization': ['ENG', 'HIN', 'SST']
            }
        ]

        created_teachers = []
        for t in teachers_data:
            u, u_created = User.objects.get_or_create(
                username=t['username'],
                defaults={
                    'first_name': t['first_name'],
                    'last_name': t['last_name'],
                    'email': t['email']
                }
            )
            if u_created:
                u.set_password('teacher@123')
                u.save()
            UserProfile.objects.get_or_create(user=u, defaults={'role': 'teacher', 'phone': t['phone']})

            tch, _ = Teacher.objects.get_or_create(
                teacher_id=t['teacher_id'],
                defaults={
                    'user': u,
                    'phone': t['phone'],
                    'qualification': t['qualification'],
                    'experience': t['experience'],
                    'bio': t['bio'],
                    'joining_date': datetime.date(2021, 4, 1),
                    'is_active': True
                }
            )
            for scode in t['specialization']:
                if scode in created_subjects:
                    tch.specialization.add(created_subjects[scode])
            created_teachers.append(tch)
        self.stdout.write(self.style.SUCCESS(f"Created {len(created_teachers)} Teachers (Password: teacher@123)."))

        # 5. Sample Batches (5 Batches)
        today = timezone.now().date()
        start_d = datetime.date(today.year, 4, 1)
        end_d = datetime.date(today.year + 1, 3, 31)

        batches_data = [
            {
                'name': 'CBSE Class 10 Morning Batch',
                'course': created_courses['CBSE Class 10 Foundation & Board Excel'],
                'board': 'CBSE',
                'class_level': '10',
                'teacher': created_teachers[0], # Pinku Raj
                'max_students': 30,
                'status': 'active'
            },
            {
                'name': 'CBSE Class 12 Science Batch',
                'course': created_courses['CBSE Class 12 Science Master Batch (PCM/PCB)'],
                'board': 'CBSE',
                'class_level': '12',
                'teacher': created_teachers[1], # Amit Sharma
                'max_students': 30,
                'status': 'active'
            },
            {
                'name': 'Bihar Board Class 10 Evening Batch',
                'course': created_courses['Bihar Board Matric (10th) Topper Batch'],
                'board': 'BIHAR',
                'class_level': '10',
                'teacher': created_teachers[0], # Pinku Raj
                'max_students': 35,
                'status': 'active'
            },
            {
                'name': 'Bihar Board Class 12 Science Batch',
                'course': created_courses['Bihar Board Inter (12th) Science I.Sc Special'],
                'board': 'BIHAR',
                'class_level': '12',
                'teacher': created_teachers[2], # Priya Verma
                'max_students': 35,
                'status': 'active'
            },
            {
                'name': 'CBSE Class 9 Foundation Batch',
                'course': created_courses['CBSE Class 9 Conceptual Foundation Program'],
                'board': 'CBSE',
                'class_level': '9',
                'teacher': created_teachers[3], # Rajesh Kumar
                'max_students': 25,
                'status': 'active'
            }
        ]

        created_batches = []
        for b in batches_data:
            batch, _ = Batch.objects.get_or_create(
                name=b['name'],
                defaults={
                    'course': b['course'],
                    'board': b['board'],
                    'class_level': b['class_level'],
                    'teacher': b['teacher'],
                    'start_date': start_d,
                    'end_date': end_d,
                    'max_students': b['max_students'],
                    'status': b['status']
                }
            )
            created_batches.append(batch)
        self.stdout.write(self.style.SUCCESS(f"Created {len(created_batches)} Batches."))

        # 6. Sample Students (10+ Students across CBSE and Bihar Board)
        students_data = [
            {'name': 'Rohan Kumar', 'id': 'NS-STU-001', 'roll': '101', 'board': 'CBSE', 'class': '10', 'batch_idx': 0, 'father': 'Sanjay Kumar', 'mobile': '9123456701', 'gender': 'M'},
            {'name': 'Sneha Kumari', 'id': 'NS-STU-002', 'roll': '102', 'board': 'CBSE', 'class': '10', 'batch_idx': 0, 'father': 'Manoj Prasad', 'mobile': '9123456702', 'gender': 'F'},
            {'name': 'Aman Verma', 'id': 'NS-STU-003', 'roll': '103', 'board': 'CBSE', 'class': '10', 'batch_idx': 0, 'father': 'Rakesh Verma', 'mobile': '9123456703', 'gender': 'M'},
            {'name': 'Pooja Singh', 'id': 'NS-STU-004', 'roll': '121', 'board': 'CBSE', 'class': '12', 'batch_idx': 1, 'father': 'Dharmendra Singh', 'mobile': '9123456704', 'gender': 'F'},
            {'name': 'Vikas Raj', 'id': 'NS-STU-005', 'roll': '122', 'board': 'CBSE', 'class': '12', 'batch_idx': 1, 'father': 'Sunil Raj', 'mobile': '9123456705', 'gender': 'M'},
            {'name': 'Anjali Gupta', 'id': 'NS-STU-006', 'roll': '201', 'board': 'BIHAR', 'class': '10', 'batch_idx': 2, 'father': 'Bijay Gupta', 'mobile': '9123456706', 'gender': 'F'},
            {'name': 'Deepak Kumar', 'id': 'NS-STU-007', 'roll': '202', 'board': 'BIHAR', 'class': '10', 'batch_idx': 2, 'father': 'Rameshwar Roy', 'mobile': '9123456707', 'gender': 'M'},
            {'name': 'Kavita Kumari', 'id': 'NS-STU-008', 'roll': '203', 'board': 'BIHAR', 'class': '10', 'batch_idx': 2, 'father': 'Santosh Sharma', 'mobile': '9123456708', 'gender': 'F'},
            {'name': 'Manish Yadav', 'id': 'NS-STU-009', 'roll': '221', 'board': 'BIHAR', 'class': '12', 'batch_idx': 3, 'father': 'Lalita Yadav', 'mobile': '9123456709', 'gender': 'M'},
            {'name': 'Priyanshu Singh', 'id': 'NS-STU-010', 'roll': '222', 'board': 'BIHAR', 'class': '12', 'batch_idx': 3, 'father': 'Arun Singh', 'mobile': '9123456710', 'gender': 'M'},
            {'name': 'Neha Patel', 'id': 'NS-STU-011', 'roll': '901', 'board': 'CBSE', 'class': '9', 'batch_idx': 4, 'father': 'Ashok Patel', 'mobile': '9123456711', 'gender': 'F'},
            {'name': 'Rahul Mishra', 'id': 'NS-STU-012', 'roll': '902', 'board': 'CBSE', 'class': '9', 'batch_idx': 4, 'father': 'Dinesh Mishra', 'mobile': '9123456712', 'gender': 'M'},
        ]

        created_students = []
        for s in students_data:
            uname = s['id'].lower().replace('-', '_')
            first_name, last_name = s['name'].split(' ', 1)
            target_batch = created_batches[s['batch_idx']]
            target_course = target_batch.course

            u, u_created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{uname}@student.nsclasses.edu"
                }
            )
            if u_created:
                u.set_password('student@123')
                u.save()

            UserProfile.objects.get_or_create(user=u, defaults={'role': 'student', 'phone': s['mobile']})

            st, _ = Student.objects.get_or_create(
                student_id=s['id'],
                defaults={
                    'user': u,
                    'roll_number': s['roll'],
                    'board': s['board'],
                    'class_level': s['class'],
                    'course': target_course,
                    'batch': target_batch,
                    'father_name': s['father'],
                    'mother_name': 'Smt. ' + s['father'].split()[0] + ' Devi',
                    'phone': s['mobile'],
                    'parent_phone': '9876' + s['mobile'][4:],
                    'gender': s['gender'],
                    'address': 'Main Town, District Bihar, India',
                    'date_of_birth': datetime.date(2009, 5, 15),
                    'is_active': True
                }
            )
            created_students.append(st)

            # Sample Fee Record
            paid_val = target_course.fees if s['roll'] in ['101', '201', '221'] else target_course.fees / 2
            FeeRecord.objects.get_or_create(
                student=st,
                defaults={
                    'total_fee': target_course.fees,
                    'paid_amount': paid_val,
                    'payment_date': today,
                    'payment_method': 'cash',
                    'remarks': 'First Term Installment Settled'
                }
            )

            # Sample Attendance Records
            for day_offset in range(1, 8):
                att_date = today - datetime.timedelta(days=day_offset)
                Attendance.objects.get_or_create(
                    student=st,
                    batch=target_batch,
                    date=att_date,
                    defaults={
                        'status': 'present' if day_offset % 6 != 0 else 'absent',
                        'marked_by': admin_user
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_students)} Students with Fee & Attendance records (Password: student@123)."))

        # 7. Separate Timetable for Every Batch (Requirement 6)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        timetable_plan = [
            # Batch 0: CBSE 10 Morning
            (created_batches[0], [
                ('Monday', 'MATH', created_teachers[0], '07:30', '08:30', 'Room 101'),
                ('Monday', 'PHYS', created_teachers[1], '08:30', '09:30', 'Room 101'),
                ('Tuesday', 'CHEM', created_teachers[2], '07:30', '08:30', 'Room 101'),
                ('Tuesday', 'MATH', created_teachers[0], '08:30', '09:30', 'Room 101'),
                ('Wednesday', 'BIO', created_teachers[3], '07:30', '08:30', 'Room 101'),
                ('Wednesday', 'ENG', created_teachers[4], '08:30', '09:30', 'Room 101'),
                ('Thursday', 'MATH', created_teachers[0], '07:30', '08:30', 'Room 101'),
                ('Thursday', 'PHYS', created_teachers[1], '08:30', '09:30', 'Room 101'),
                ('Friday', 'CHEM', created_teachers[2], '07:30', '08:30', 'Room 101'),
                ('Friday', 'MATH', created_teachers[0], '08:30', '09:30', 'Room 101'),
                ('Saturday', 'SST', created_teachers[4], '07:30', '09:30', 'Room 101'),
            ]),
            # Batch 1: CBSE 12 Science
            (created_batches[1], [
                ('Monday', 'PHYS', created_teachers[1], '09:45', '11:00', 'Room 201'),
                ('Monday', 'CHEM', created_teachers[2], '11:00', '12:15', 'Room 201'),
                ('Tuesday', 'MATH', created_teachers[0], '09:45', '11:00', 'Room 201'),
                ('Tuesday', 'PHYS', created_teachers[1], '11:00', '12:15', 'Room 201'),
                ('Wednesday', 'CHEM', created_teachers[2], '09:45', '11:00', 'Room 201'),
                ('Wednesday', 'BIO', created_teachers[3], '11:00', '12:15', 'Room 201'),
                ('Thursday', 'PHYS', created_teachers[1], '09:45', '11:00', 'Room 201'),
                ('Friday', 'MATH', created_teachers[0], '09:45', '11:00', 'Room 201'),
                ('Saturday', 'ENG', created_teachers[4], '09:45', '11:00', 'Room 201'),
            ]),
            # Batch 2: Bihar Board 10 Evening
            (created_batches[2], [
                ('Monday', 'MATH', created_teachers[0], '15:30', '16:45', 'Hall A'),
                ('Monday', 'SCI', created_teachers[1], '16:45', '18:00', 'Hall A'),
                ('Tuesday', 'HIN', created_teachers[4], '15:30', '16:45', 'Hall A'),
                ('Tuesday', 'MATH', created_teachers[0], '16:45', '18:00', 'Hall A'),
                ('Wednesday', 'SCI', created_teachers[3], '15:30', '16:45', 'Hall A'),
                ('Wednesday', 'SST', created_teachers[4], '16:45', '18:00', 'Hall A'),
                ('Thursday', 'MATH', created_teachers[0], '15:30', '16:45', 'Hall A'),
                ('Friday', 'SCI', created_teachers[2], '15:30', '16:45', 'Hall A'),
                ('Saturday', 'ENG', created_teachers[4], '15:30', '17:00', 'Hall A'),
            ]),
            # Batch 3: Bihar Board 12 Science
            (created_batches[3], [
                ('Monday', 'PHYS', created_teachers[1], '16:00', '17:15', 'Room 202'),
                ('Monday', 'CHEM', created_teachers[2], '17:15', '18:30', 'Room 202'),
                ('Tuesday', 'MATH', created_teachers[0], '16:00', '17:15', 'Room 202'),
                ('Wednesday', 'BIO', created_teachers[3], '16:00', '17:15', 'Room 202'),
                ('Thursday', 'CHEM', created_teachers[2], '16:00', '17:15', 'Room 202'),
                ('Friday', 'PHYS', created_teachers[1], '16:00', '17:15', 'Room 202'),
                ('Saturday', 'HIN', created_teachers[4], '16:00', '17:15', 'Room 202'),
            ]),
            # Batch 4: CBSE 9 Foundation
            (created_batches[4], [
                ('Monday', 'MATH', created_teachers[0], '14:00', '15:15', 'Room 102'),
                ('Tuesday', 'SCI', created_teachers[3], '14:00', '15:15', 'Room 102'),
                ('Wednesday', 'MATH', created_teachers[0], '14:00', '15:15', 'Room 102'),
                ('Thursday', 'SCI', created_teachers[1], '14:00', '15:15', 'Room 102'),
                ('Friday', 'ENG', created_teachers[4], '14:00', '15:15', 'Room 102'),
            ])
        ]

        total_slots = 0
        for batch_obj, slots in timetable_plan:
            for day, scode, teacher_obj, s_time, e_time, rm in slots:
                st_time_obj = datetime.datetime.strptime(s_time, '%H:%M').time()
                end_time_obj = datetime.datetime.strptime(e_time, '%H:%M').time()
                TimetableEntry.objects.get_or_create(
                    batch=batch_obj,
                    day=day,
                    start_time=st_time_obj,
                    defaults={
                        'subject': created_subjects[scode],
                        'teacher': teacher_obj,
                        'end_time': end_time_obj,
                        'room': rm
                    }
                )
                total_slots += 1
        self.stdout.write(self.style.SUCCESS(f"Created {total_slots} Timetable Slots across all separate batches."))

        # 8. Sample Announcements
        announcements_data = [
            {
                'title': 'New Academic Batches 2026-27 Commencing Next Week',
                'description': 'Orientation and batch start for CBSE and Bihar Board Classes 9, 10, 11, and 12 begin on Monday. Students must collect their ID cards and timetable handbook.',
                'target_audience': 'all',
                'priority': 'important'
            },
            {
                'title': 'CBSE Class 10 Science & Math Special Sunday Mock Exam',
                'description': 'Full syllabus 3-hour mock board test on Sunday at 9:00 AM in Hall A. Attendance is compulsory for all enrolled CBSE Class 10 students.',
                'target_audience': 'batch',
                'batch': created_batches[0],
                'priority': 'urgent'
            },
            {
                'title': 'Bihar Board Matric Special Objective Question Workshop',
                'description': 'Director Pinku Raj will conduct an exclusive 50-mark objective scoring strategy seminar this Friday from 4:00 PM to 6:00 PM.',
                'target_audience': 'batch',
                'batch': created_batches[2],
                'priority': 'important'
            },
            {
                'title': 'Faculty Coordination Meeting with Director Pinku Raj',
                'description': 'All teachers must attend the monthly academic progress review meeting in the Director chamber on Saturday after classes.',
                'target_audience': 'teachers',
                'priority': 'normal'
            }
        ]
        for ann in announcements_data:
            Announcement.objects.get_or_create(
                title=ann['title'],
                defaults={
                    'description': ann['description'],
                    'target_audience': ann['target_audience'],
                    'batch': ann.get('batch'),
                    'priority': ann['priority'],
                    'created_by': admin_user,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS("Created Sample Announcements."))

        # 9. Sample Testimonials
        testimonials_data = [
            {'name': 'Rohan Kumar', 'course': 'CBSE Class 10 (96.4% in Board)', 'rating': 5, 'review': 'NS Classes transformed my understanding of Mathematics and Physics. Pinku Sir teaches concepts from ground up and makes every formula simple.'},
            {'name': 'Anjali Gupta', 'course': 'Bihar Board Matric (District Rank 3)', 'rating': 5, 'review': 'The separate batches and objective question test series at NS Classes helped me score top marks in BSEB board exams. Truly the best coaching!'},
            {'name': 'Pooja Singh', 'course': 'CBSE Class 12 Science (95% in Board)', 'rating': 5, 'review': 'Dedicated faculty, clear timetable, and personal attention made all the difference in my Class 12 board preparations.'},
            {'name': 'Deepak Kumar', 'course': 'Bihar Board 10th (462/500)', 'rating': 5, 'review': 'Pinku Sir mentorship and daily practice sheets gave me huge confidence. Highly recommend NS Classes to every student.'},
        ]
        for t in testimonials_data:
            Testimonial.objects.get_or_create(
                student_name=t['name'],
                defaults={
                    'course_class': t['course'],
                    'rating': t['rating'],
                    'review': t['review'],
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS("Created Sample Testimonials."))

        # 10. Sample Gallery Items
        gallery_data = [
            {'title': 'Classroom Conceptual Learning Session', 'category': 'classroom', 'description': 'Interactive mathematics lecture conducted by Director Pinku Raj.'},
            {'title': 'Annual Board Toppers Felicitation Ceremony', 'category': 'achievements', 'description': 'Awarding medals and scholarships to CBSE & Bihar Board merit holders.'},
            {'title': 'Science Laboratory Demonstration Workshop', 'category': 'activities', 'description': 'Practical physics and chemistry demonstrations for Class 10 & 12 students.'},
            {'title': 'Exam Strategy & Time Management Seminar', 'category': 'seminars', 'description': 'Special guidance workshop on maximizing board exam scores.'},
            {'title': 'Weekly Mock Test & Evaluation Hall', 'category': 'events', 'description': 'Disciplined exam environment simulation for board aspirants.'},
            {'title': 'Doubt Clearance & Personal Mentorship Hour', 'category': 'classroom', 'description': 'One-on-one problem solving with expert faculty.'},
        ]
        for g in gallery_data:
            Gallery.objects.get_or_create(
                title=g['title'],
                defaults={
                    'category': g['category'],
                    'description': g['description'],
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS("Created Sample Gallery Entries."))

        # 11. Sample Admission Enquiries
        enquiries_data = [
            {'name': 'Vikram Mehra', 'parent': 'Kishore Mehra', 'phone': '9876501234', 'email': 'vikram@gmail.com', 'board': 'CBSE', 'class': '10', 'course': 'CBSE Class 10 Science & Math', 'status': 'new', 'message': 'Interested in morning batch for Class 10 CBSE.'},
            {'name': 'Swati Sinha', 'parent': 'Pradeep Sinha', 'phone': '9876501235', 'email': 'swati@gmail.com', 'board': 'BIHAR', 'class': '12', 'course': 'Bihar Board 12th I.Sc', 'status': 'contacted', 'message': 'Want details regarding physics and chemistry batches.'},
            {'name': 'Abhishek Pandey', 'parent': 'Nandlal Pandey', 'phone': '9876501236', 'email': 'abhishek@gmail.com', 'board': 'CBSE', 'class': '12', 'course': 'CBSE Class 12 PCM', 'status': 'interested', 'message': 'Requested fee installment details.'},
            {'name': 'Simran Kaur', 'parent': 'Gurjeet Singh', 'phone': '9876501237', 'email': 'simran@gmail.com', 'board': 'BIHAR', 'class': '10', 'course': 'Bihar Board Matric Topper', 'status': 'admitted', 'message': 'Admission confirmed and batch assigned.'},
        ]
        for e in enquiries_data:
            AdmissionEnquiry.objects.get_or_create(
                student_name=e['name'],
                defaults={
                    'parent_name': e['parent'],
                    'phone': e['phone'],
                    'email': e['email'],
                    'board': e['board'],
                    'class_level': e['class'],
                    'interested_course': e['course'],
                    'status': e['status'],
                    'message': e['message']
                }
            )

        # 12. Sample FAQs
        faqs_data = [
            {'q': 'What educational boards does NS Classes provide preparation for?', 'a': 'NS Classes provides comprehensive academic coaching and preparation for both CBSE Board and Bihar Board (BSEB) students from Class 6 to Class 12.', 'order': 1},
            {'q': 'Are there separate batches for CBSE and Bihar Board students?', 'a': 'Yes, absolutely. We maintain distinct, dedicated batches for CBSE and Bihar Board with separate syllabus plans, lecture timings, and study materials.', 'order': 2},
            {'q': 'How does NS Classes track student attendance?', 'a': 'Faculty members take attendance daily in our portal system. Parents and students can monitor their attendance percentage and present/absent history via their student dashboard.', 'order': 3},
            {'q': 'Who is the Director of NS Classes and how can I reach out?', 'a': 'The Director and Academic Head of NS Classes is Pinku Raj. You can reach the institute directly via phone at +91 987654321 or through our official website contact form.', 'order': 4},
            {'q': 'How can students download study notes and sample question papers?', 'a': 'Enrolled students can log in to their student portal dashboard and navigate to the Study Notes repository to view and download chapter notes, assignments, and sample papers.', 'order': 5},
        ]
        for f in faqs_data:
            FAQ.objects.get_or_create(
                question=f['q'],
                defaults={
                    'answer': f['a'],
                    'order': f['order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('\n========================================='))
        self.stdout.write(self.style.SUCCESS('SAMPLE DATA SUCCESSFULLY POPULATED!'))
        self.stdout.write(self.style.SUCCESS('========================================='))
        self.stdout.write(self.style.NOTICE('Admin Login:   admin / admin123'))
        self.stdout.write(self.style.NOTICE('Teacher Login: pinku_raj / teacher@123 (or amit_sharma, priya_verma)'))
        self.stdout.write(self.style.NOTICE('Student Login: ns_stu_001 / student@123 (or ns_stu_002, ns_stu_006)'))
