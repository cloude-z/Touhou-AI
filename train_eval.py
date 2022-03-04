import torch
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')

def PokeAIMaster(model, epochs, train_loader, cv_loader):
    """
    Training the model and evaluating by the cross-validation set. The function will
    record the training loss and cv loss to futher check the performance of the model.
    """
    losses = []
    cv_losses = []
    
    for e in range(epochs):
        print(f"\rEpoch: {e:2d}  " + "="*20)
        
        loss = model_train(model, train_loader)
        cv_loss = model_eval(model, cv_loader)
        
        losses.append(loss)
        cv_losses.append(cv_loss)
        
        print(f"loss: {loss:>5.2f}, cv_loss: {cv_loss:>5.2f}")
    
    # 学一下怎么画图画的更好
    plt.plot(range(epochs), losses, range(epochs), cv_losses)
    
    return losses, cv_losses

def model_train(model, train_loader):
    model.train()
    size = len(train_loader.dataset)
    batch_size = train_loader.batch_size

    for batch, (x, y) in enumerate(train_loader):
        model.optimizer.zero_grad()
        x, y = x.to(device), y.to(device)
        
        pred = model(x)
        loss = model.criterion(pred, y)
        loss.backward()
        model.optimizer.step()

#         if batch % 20 == 0:
#             print(f"training --> {batch_size*batch:>5d}/{size:>5d}, loss --> {loss.item():>5.3f}")
    
    return loss.item()

def model_eval(model, cv_loader):
    model.eval()
    cv_loss_avg = 0
    num_batch = len(cv_loader)
    
    with torch.no_grad():
        for x, y in cv_loader:
            x, y = x.to(device), y.to(device)
            
            pred = model(x)
            cv_loss = model.criterion(pred, y)
            cv_loss_avg += cv_loss.item()
    
    cv_loss_avg /= num_batch
    
    return cv_loss_avg


def model_test(model, test_loader):
    # 分类精度损失等
    model.eval()

    pass