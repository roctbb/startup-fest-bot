from manage import app
from methods.projects import *
from methods.users import *
import segno

with app.app_context():
    projects = get_all_projects()
    users = get_all_users()

    for project in projects:
        if not project.users:
            continue

        expert_transactions = filter(lambda t: t.user.role == 'expert', project.investments)
        student_transactions = filter(lambda t: t.user.role == 'student', project.investments)

        per_user_expert_investment = sum(map(lambda transaction: -1 * transaction.amount, expert_transactions)) // len(
            project.users)
        per_user_student_investment = sum(
            map(lambda transaction: -1 * transaction.amount, student_transactions)) // len(project.users)

        if per_user_expert_investment:
            for user in project.users:
                make_transaction(user, per_user_expert_investment, 'PCE',
                                 f'Инвестиции в проект {project.name} от экспертов')

        if per_user_student_investment:
            for user in project.users:
                make_transaction(user, per_user_student_investment, 'PCS',
                                 f'Инвестиции в проект {project.name} от гостей')

    for user in filter(lambda u: u.telegram_id, users):
        qrcode = segno.make_qr(user.payment_code)
        filename = f"./payment_qrs/{user.id}.png"
        qrcode.save(filename, scale=10)

        send_telegram_notification(user, f"Ваш баланс:\n\n💵 {user.balance('PCS')} PCS\n💶 {user.balance('PCE')} PCE",
                                   open(filename, 'rb').read())
