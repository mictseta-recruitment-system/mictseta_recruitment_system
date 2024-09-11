from django.shortcuts import render
from jobs.models import JobPost, SkillList
from profiles.models import SupportingDocuments
# Create your views here.
def job_seeker_dashboard(request):
    return render(request, 'job_seeker_dashboard.html')

def personal_details(request):
    return render(request, 'personal_details.html')
def address_details(request):
    return render(request, 'address_details.html')

def academic_qualifications(request):
    return render(request, 'academic_qualifications.html')

def language_proficiency(request):
    return render(request, 'language_proficiency.html')

def soft_skills(request):
    skill_List = [
        {
            "skill_name": "Java programming",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Python programming ",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "C# programming ",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "C++ programming ",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "JavaScript programming",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Git version control ",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Jenkins automation",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Docker containerization",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Microservices architecture",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "RESTful web services development",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cloud computing with AWS and Microsoft Azure",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Agile project management methodology",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Scrum project management methodology",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "DevOps practices",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "MySQL database management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "PostgreSQL database management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "MongoDB database management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Oracle database management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Microsoft SQL Server management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "IntelliJ IDEA usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Visual Studio usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Eclipse IDE usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "TCP/IP knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "DNS configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "DHCP configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "VPN setup and management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "SSL/TLS encryption",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cisco IOS usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cisco routers and switches configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Firewall configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Intrusion Detection Systems (IDS)",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Intrusion Prevention Systems (IPS)",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "LAN and WAN setup",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "VLAN configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "SD-WAN configuration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "VMware virtualization",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Hyper-V virtualization",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "CompTIA Network Plus certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cisco Certified Network Associate (CCNA) certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cisco Certified Network Professional (CCNP) certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Systems analysis and design",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Enterprise resource planning systems (SAP, Oracle) knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Business process modeling",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Unified Modeling Language (UML) diagramming",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Microsoft Visio usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "AWS cloud services",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Google Cloud platform usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Microsoft Azure cloud services",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cybersecurity principles",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Network security tools",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Risk management frameworks (ISO 27001, NIST, GDPR)",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Encryption and cryptography",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Ethical hacking and penetration testing",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "CompTIA Security Plus certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "CISSP certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Certified Ethical Hacker certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "System architecture and integration",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Cloud-based application development",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "System debugging and optimization",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Puppet configuration management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Ansible configuration management",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Microsoft Project usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Trello project management tool usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Jira project management tool usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Asana project management tool usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "PRINCE2 certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "PMP certification knowledge",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Budgeting and scheduling software usage",
            "skill_type": "computer skill"
        },
        {
            "skill_name": "Risk assessment tools usage",
            "skill_type": "computer skill"
        },
        
        {
            "skill_name": "Problem-solving",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Analytical thinking",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Team collaboration",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Effective communication",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Attention to detail",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Critical thinking",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Flexibility and adaptability",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Time management",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Leadership",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Negotiation skills",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Organizational skills",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Documentation and report writing",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Stakeholder liaison",
            "skill_type": "soft skill"
        },
        {
            "skill_name": "Risk management",
            "skill_type": "soft skill"
        }
    ]
 
    for skill in skill_List:
        skill_to_add= SkillList.objects.get(skill_name=skill['skill_name'],skill_type=['skill_type'] )
        skill.save

    return render(request, 'soft_skills.html')

def computer_skills(request):
    return render(request, 'computer_skills.html')

def working_experience(request):
    return render(request, 'working_experience.html')

def referees(request):
    return render(request, 'referees.html')

def supporting_documents(request):
    docs = SupportingDocuments.objects.filter(user=request.user)
    return render(request, 'supporting_documents.html',{"docs":docs})

def job_details(request):
    job_list = JobPost.objects.filter(status='open')
    return render(request, 'jobseeker_job_details.html', {'job_list':job_list})

def application_tracking(request):
    return render(request, 'application_tracking.html')

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request, jobID):
    jobs = JobPost.objects.filter(id=jobID).first()
    return render(request, 'job_information.html', {'jobs':jobs})

def feedback(request):
    return render(request, 'feedback.html')

def logout(request):
    return render(request, 'logout.html')



